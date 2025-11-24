from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_user, get_current_admin_user
from app.users.models import User
from app.subscriptions.dao import SubscriptionDAO
from app.memberships.dao import MembershipDAO, SubRequestDAO
from app.memberships.schemas import (SMembershipCreate, SSubReqUpdate, SSubReqInfo, SMembershipInfo,
                                     SSubReqCreate, SFilter, SSubReqFilter, SSubReqInfoFull, SSubReqAdd)
from app.exceptions import (RequestOnlyClient, SubNotFound, MembershipIsActive, RequestIsPending,
                            RequestNotFound, RequestAlreadyAccept, RequestBadStatus)


router = APIRouter(prefix="/memberships", tags=["Memberships"])

@router.post("/request/", response_model=SSubReqInfo, status_code=201, summary="Создать заявку на абонемент")
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
    filters = SFilter(user_id=user_data.id, status="active")
    active_membership = await membership_dao.find_one_or_none(filters=filters)
    if active_membership:
        raise MembershipIsActive
    # Если есть активная заявка, то подать новую заявку нельзя
    filters = SFilter(user_id=user_data.id, status="pending")
    existing_request = await sr_dao.find_one_or_none(filters=filters)
    if existing_request:
        raise RequestIsPending
    # Создание заявки 
    values = SSubReqAdd(user_id=user_data.id, subscription_id=data.subscription_id)
    new_request = await sr_dao.add(values=values)
    return new_request

@router.patch("/request/{request_id}/", summary="Изменить статус заявки на абонемент")
async def update_sub_request_status(request_id: int,
                                    data: SSubReqUpdate,
                                    session: AsyncSession = Depends(get_session_with_commit),
                                    user_data: User = Depends(get_current_admin_user)
                                    ) -> SSubReqInfo | dict:
    """
    Админ изменяет статус заявки клиента на абонемент.
    Доступ только у админа.
    """
    sr_dao = SubRequestDAO(session)
    sub_dao = SubscriptionDAO(session)
    membership_dao = MembershipDAO(session)
    # Проверка существования заявки
    request = await sr_dao.find_one_or_none_by_id(request_id)
    if not request:
        raise RequestNotFound
    if request.status != "pending":
        raise RequestAlreadyAccept
    # Изменение статуса заявки
    if data.status == "approved":
        subscription = await sub_dao.find_one_or_none_by_id(request.subscription_id)

        start_date = date.today()
        end_date = start_date + timedelta(days=subscription.duration_days)

        values = SMembershipCreate(
            user_id=request.user_id,
            subscription_id=request.subscription_id,
            start_date=start_date,
            end_date=end_date,
            status="active"
        )
        new_membership = await membership_dao.add(values=values)
        if not new_membership:
            return {"message": "Ошибка при создании membership"}
    elif data.status == "rejected":
        pass
    else:
        raise RequestBadStatus
    # Изменение статуса заявки
    filters = SSubReqFilter(id=request_id)
    updated_count = await sr_dao.update(
        filters=filters,
        values=data
    )
    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")

    updated_request = await sr_dao.find_one_or_none_by_id(request_id)
    return SSubReqInfo.model_validate(updated_request)

@router.get("/request/", response_model=list[SSubReqInfoFull], summary="Получить список всех заявок")
async def get_all_requests(session: AsyncSession = Depends(get_session_without_commit),
                           user_data: User = Depends(get_current_admin_user)):
    """
    Возвращает список всех существующих заявок.
    Доступ только у админа.
    """
    return await SubRequestDAO(session).find_requests_with_data()