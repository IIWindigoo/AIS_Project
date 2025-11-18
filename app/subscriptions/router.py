from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.subscriptions.dao import SubscriptionDAO
from app.subscriptions.schemas import SSubInfo, SSubFilter, SSubUpd, SSubAdd
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_admin_user
from app.exceptions import SubNotFound
from app.users.models import User


router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/", summary="Получить все абонементы")
async def get_all_subscriptions(session: AsyncSession = Depends(get_session_without_commit)
                                ) -> list[SSubInfo]:
    """
    Возвращает список всех существующих абонементов.
    Доступ у всех
    """
    return await SubscriptionDAO(session).find_all()

@router.post("/", summary="Создать абонемент")
async def create_subscription(sub_data: SSubAdd,
                              session: AsyncSession = Depends(get_session_with_commit),
                              user_data: User = Depends(get_current_admin_user)
                              ) -> SSubInfo | dict:
    """
    Создает новый абонемент.
    Доступ только у администратора 
    """
    new_sub = await SubscriptionDAO(session).add(values=sub_data)
    if new_sub:
        return SSubInfo.model_validate(new_sub)
    return {"message": "Ошибка при создании абонемента"}

@router.delete("/{sub_id}/", summary="Удалить абонемент по ID")
async def delete_sub(sub_id: int,
                      session: AsyncSession = Depends(get_session_with_commit),
                      user_data: User = Depends(get_current_admin_user)
                      ) -> dict:
    """
    Удаление конкретного абонемента по ID.
    Доступ только у администратора
    """
    sub_dao = SubscriptionDAO(session)
    # Проверка существования абонемента
    sub = await sub_dao.find_one_or_none_by_id(sub_id)
    if not sub:
        raise SubNotFound
    # Удаление абонемента
    filters = SSubFilter(id=sub_id)
    deleted_count = await sub_dao.delete(filters=filters)
    if deleted_count:
        return {
            "message": f"Абонемент [{sub.title}] успешно удален",
            "deleted_count": deleted_count,
            "deleted_sub": {
                "id": sub.id,
                "title": sub.title,
                "price": sub.price,
                "duration_days": sub.duration_days,
            }
        }
    return {"message": "Ошибка при удалении абонемента"}

@router.patch("/{sub_id}/", summary="Изменить абонемент по ID")
async def update_sub(sub_id: int,
                      data: SSubUpd,
                      session: AsyncSession = Depends(get_session_with_commit),
                      user_data: User = Depends(get_current_admin_user)
                      ) -> SSubInfo:
    """
    Изменение информации об абонемента по ID.
    Доступ только у администратора
    """
    sub_dao = SubscriptionDAO(session)
    # Проверка существования абонемента
    sub = await sub_dao.find_one_or_none_by_id(sub_id)
    if not sub:
        raise SubNotFound
    # Обновление информации о абонементе
    filters = SSubFilter(id=sub_id)
    update_values = SSubUpd(**data.model_dump(exclude_unset=True))
    updated_count = await sub_dao.update(
        filters=filters,
        values=update_values
    )
    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")
    updated = await sub_dao.find_one_or_none_by_id(sub_id)
    return SSubInfo.model_validate(updated)