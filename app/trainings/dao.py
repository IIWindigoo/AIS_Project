from app.dao.base import BaseDAO
from app.trainings.models import Training
from app.bookings.models import Booking

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger


class TrainingDAO(BaseDAO):
    model = Training

    async def find_by_trainer_with_clients(self, trainer_id: int):
        logger.info(f"Поиск тренировок для тренера {trainer_id} с загрузкой клиентов")
        try:
            query = (
                select(self.model)
                .where(self.model.trainer_id == trainer_id)
                .options(
                    selectinload(self.model.bookings).selectinload(Booking.user)
                )
            )
            result = await self._session.execute(query)
            trainings = result.scalars().all()
            logger.info(f"Найдено {len(trainings)} тренировок для тренера {trainer_id}")
            return trainings
        except Exception as e:
            logger.error(f"Ошибка при поиске тренировок тренера {trainer_id}: {e}")
            raise