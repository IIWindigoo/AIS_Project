from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.rooms.schemas import SRoomInfo, SRoomFilter, SRoomUpd, SRoomAdd
from app.rooms.dao import RoomDAO
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_admin_user
from app.exceptions import RoomNotFound
from app.users.models import User


router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", summary="Получить все помещения")
async def get_all_rooms(session: AsyncSession = Depends(get_session_without_commit)) -> list[SRoomInfo]:
    """
    Возвращает список всех существующих помещений
    Доступ для всех пользователей
    """
    return await RoomDAO(session).find_all()

@router.post("/", summary="Создать помещение")
async def create_room(room_data: SRoomAdd,
                      session: AsyncSession = Depends(get_session_with_commit),
                      user_data: User = Depends(get_current_admin_user)
                      ) -> SRoomInfo | dict:
    """
    Создает новое помещение.
    Доступ только у администратора 
    """
    new_room = await RoomDAO(session).add(values=room_data)
    if new_room:
        return SRoomInfo.model_validate(new_room)
    return {"message": "Ошибка при добавлении помещения"}

@router.delete("/{room_id}/", summary="Удалить помешение")
async def delete_room(room_id: int,
                      session: AsyncSession = Depends(get_session_with_commit),
                      user_data: User = Depends(get_current_admin_user)
                      ) -> dict:
    """
    Удаление конкретного помещения по ID.
    Доступ только у администратора
    """
    room_dao = RoomDAO(session)
    # Проверка существования помещения
    room = await room_dao.find_one_or_none_by_id(room_id)
    if not room:
        raise RoomNotFound
    # Удаление помещения
    filters = SRoomFilter(id=room_id)
    deleted_count = await room_dao.delete(filters=filters)
    if deleted_count:
        return {
            "message": f"Помещение [{room.title}] успешно удалено",
            "deleted_count": deleted_count,
            "deleted_room": {
                "id": room.id,
                "title": room.title,
                "capacity": room.capacity
            }
        }
    return {"message": "Ошибка при удалении помещения"}

@router.patch("/{room_id}/", summary="Изменить помещение")
async def update_room(room_id: int,
                      data: SRoomUpd,
                      session: AsyncSession = Depends(get_session_with_commit),
                      user_data: User = Depends(get_current_admin_user)
                      ) -> SRoomInfo:
    """
    Изменение информации о помещении по ID.
    Доступ только у администратора
    """
    room_dao = RoomDAO(session)
    # Проверка существования помещения
    room = await room_dao.find_one_or_none_by_id(room_id)
    if not room:
        raise RoomNotFound
    # Обновление информации о помещении
    filters = SRoomFilter(id=room_id)
    update_values = SRoomUpd(**data.model_dump(exclude_unset=True))
    updated_count = await room_dao.update(
        filters=filters,
        values=update_values
    )
    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")
    updated = await room_dao.find_one_or_none_by_id(room_id)
    return SRoomInfo.model_validate(updated)