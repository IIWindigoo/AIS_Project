from app.dao.base import BaseDAO
from app.trainings.models import Training
from app.bookings.models import Booking

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger


class TrainingDAO(BaseDAO):
    model = Training

    async def find_all(self, **filter_by):
        """Переопределяем find_all для загрузки room relationship"""
        logger.info(f"Поиск всех записей {self.model.__name__} по фильтрам: {filter_by}")
        try:
            query = select(self.model).filter_by(**filter_by).options(selectinload(self.model.room))
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except Exception as e:
            logger.error(f"Ошибка при поиске всех записей {self.model.__name__}: {e}")
            raise

    async def find_one_or_none_by_id(self, data_id: int):
        """Переопределяем find_one_or_none_by_id для загрузки room relationship"""
        logger.info(f"Поиск записи {self.model.__name__} по ID: {data_id}")
        try:
            query = select(self.model).filter_by(id=data_id).options(selectinload(self.model.room))
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись {self.model.__name__} с ID {data_id} найдена.")
            else:
                logger.warning(f"Запись {self.model.__name__} с ID {data_id} не найдена.")
            return record
        except Exception as e:
            logger.error(f"Ошибка при поиске записи {self.model.__name__} по ID {data_id}: {e}")
            raise

    async def find_by_trainer_with_clients(self, trainer_id: int):
        logger.info(f"Поиск тренировок для тренера {trainer_id} с загрузкой клиентов")
        try:
            query = (
                select(self.model)
                .where(self.model.trainer_id == trainer_id)
                .options(
                    selectinload(self.model.bookings).selectinload(Booking.user),
                    selectinload(self.model.room)
                )
            )
            result = await self._session.execute(query)
            trainings = result.scalars().all()
            logger.info(f"Найдено {len(trainings)} тренировок для тренера {trainer_id}")
            return trainings
        except Exception as e:
            logger.error(f"Ошибка при поиске тренировок тренера {trainer_id}: {e}")
            raise