from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingAdd, SBookingInfo, SBookingAddFull
from app.users.models import User
from app.dependencies.auth_dep import get_current_user
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.trainings.dao import TrainingDAO
from app.bookings.models import Booking
from app.exceptions import BookingExist, BookingOnlyClient, TrainingNotFound, BookingNotFound


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", summary="Записаться на тренировку", response_model=SBookingInfo)
async def create_booking(booking_data: SBookingAdd,
                         user_data: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session_with_commit)):
    """
    Запись на тренировку.
    Доступ только для клиента.
    """
    booking_dao = BookingDAO(session)
    training_dao = TrainingDAO(session)
    
    # Проверка роли пользователя
    if user_data.role.name != "client":
        raise BookingOnlyClient
    # Проверка существования тренировки
    training = await training_dao.find_one_or_none_by_id(booking_data.training_id)
    if not training:
        raise TrainingNotFound
    # Проверка, что пользователь не записан на тренировку
    existing = await booking_dao.find_by_user(user_data.id)
    if any(b.training_id == booking_data.training_id for b in existing):
        raise BookingExist
    # Создание записи на тренировку
    booking = await booking_dao.add(SBookingAddFull(training_id=booking_data.training_id, 
                                                   user_id=user_data.id))
    # Делаем повторный SELECT c selectinload, чтобы подтянуть training
    booking_with_training = await session.scalar(
        select(Booking)
        .options(selectinload(Booking.training))
        .where(Booking.id == booking.id)
    )
    return booking_with_training

@router.get("/", summary="Мои записи", response_model=list[SBookingInfo])
async def get_user_bookings(user_data: User = Depends(get_current_user),
                            session: AsyncSession = Depends(get_session_without_commit)):
    bookind_dao = BookingDAO(session)
    return await bookind_dao.find_by_user(user_data.id)

@router.delete("/", summary="Отменить запись", status_code=204)
async def cancel_booking(booking_data: SBookingAdd,
                         user_data: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session_with_commit)):
    booking_dao = BookingDAO(session)
    # Проверка существования записи на тренировку
    filters = SBookingAddFull(user_id=user_data.id, training_id=booking_data.training_id)
    booking = await booking_dao.find_one_or_none(filters)
    if not booking:
        raise BookingNotFound
    # Удаление записи на тренировку
    await booking_dao.delete(filters)
    return None