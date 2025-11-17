from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_user, get_current_admin_user
from app.users.models import User
from app.subscriptions.dao import SubscriptionDAO
from app.memberships.dao import MembershipDAO, SubRequestDAO
from app.memberships.schemas import (SMembershipCreate, SSubReqUpdate, SSubReqInfo, SMembershipInfo,
                                     SSubReqCreate)
from app.exceptions import (RequestOnlyClient, SubNotFound, MembershipIsActive, RequestIsPending)


router = APIRouter(prefix="/memberships", tags=["Memberships"])

@router.post("/request/", response_model=SSubReqInfo, status_code=201)
async def create_sub_request(data: SSubReqCreate,
                             session: AsyncSession = Depends(get_session_with_commit),
                             user_data: User = Depends(get_current_user)):
    """
    Клиент создает заявку на одобрение абонемента.
    Доступ у клиента.
    """
    sr_dao = SubRequestDAO(session)
    sub_dao = SubscriptionDAO(session)
    membership_dao = MembershipDAO(session)
    # Проверка, что только клиент может отправлять заявки
    if user_data.role.name != "client":
        raise RequestOnlyClient
    # Проверка существования абонемента
    subscription = await sub_dao.find_one_or_none_by_id(data.subscription_id)
    if not subscription:
        raise SubNotFound
    # Если есть активный абонемент, то подать новую заявку нельзя
    active_membership = await membership_dao.find_one_or_none(
        filters={"user_id": user_data.id, "status": "active"}
    )
    if active_membership:
        raise MembershipIsActive
    # Если есть активная заявка, то подать новую заявку нельзя
    existing_request = await sr_dao.find_one_or_none(
        filters={"user_id": user_data.id, "status": "pending"}
    )
    if existing_request:
        raise RequestIsPending
    # Создание заявки 
    new_request = await sr_dao.add(
        values={"user_id": user_data.id, "subscription_id": data.subscription_id}
    )
    return new_request