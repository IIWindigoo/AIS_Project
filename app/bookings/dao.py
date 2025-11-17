from app.dao.base import BaseDAO
from app.bookings.models import Booking

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger


class BookingDAO(BaseDAO):
    model = Booking

    async def find_by_user(self, user_id: int):
        logger.info(f"Поиск всех записей {self.model.__name__} у пользователя ID={user_id}")
        try:
            query = (select(self.model)
                        .options(selectinload(self.model.training))
                        .where(self.model.user_id == user_id))
            result = await self._session.execute(query)
            bookings = result.scalars().all()
            logger.info(f"Найдено {len(bookings)} записей.")
            return bookings
        except Exception as e:
            logger.error(f"Ошибка при поиске бронирований для user_id={user_id}: {e}")
            raise