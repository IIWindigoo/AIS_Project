from app.dao.base import BaseDAO
from app.trainings.models import Training
from app.bookings.models import Booking

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from loguru import logger
from datetime import date, time


class TrainingDAO(BaseDAO):
    model = Training

    async def find_all(self, **filter_by):
        """Переопределяем find_all для загрузки room, trainer и bookings relationships"""
        logger.info(f"Поиск всех записей {self.model.__name__} по фильтрам: {filter_by}")
        try:
            query = (
                select(self.model)
                .filter_by(**filter_by)
                .options(
                    selectinload(self.model.room),
                    selectinload(self.model.trainer),
                    selectinload(self.model.bookings)
                )
            )
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except Exception as e:
            logger.error(f"Ошибка при поиске всех записей {self.model.__name__}: {e}")
            raise

    async def find_one_or_none_by_id(self, data_id: int):
        """Переопределяем find_one_or_none_by_id для загрузки room, trainer и bookings relationships"""
        logger.info(f"Поиск записи {self.model.__name__} по ID: {data_id}")
        try:
            query = (
                select(self.model)
                .filter_by(id=data_id)
                .options(
                    selectinload(self.model.room),
                    selectinload(self.model.trainer),
                    selectinload(self.model.bookings)
                )
            )
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

    async def check_time_conflicts(
        self,
        room_id: int,
        trainer_id: int,
        training_date: date,
        start_time: time,
        end_time: time,
        exclude_training_id: int = None
    ) -> tuple[bool, str | None]:
        """
        Проверяет конфликты времени для помещения И тренера одним запросом.
        Возвращает кортеж: (есть_конфликт: bool, тип_конфликта: str | None)

        Типы конфликтов:
        - "room" - помещение занято
        - "trainer" - тренер занят
        - None - конфликтов нет
        """
        logger.info(
            f"Проверка конфликтов для помещения {room_id} и тренера {trainer_id} "
            f"на {training_date} с {start_time} до {end_time}"
        )
        try:
            # Создаем условие пересечения временных интервалов
            time_overlap = or_(
                # Новая тренировка начинается во время существующей
                and_(
                    self.model.start_time <= start_time,
                    self.model.end_time > start_time
                ),
                # Новая тренировка заканчивается во время существующей
                and_(
                    self.model.start_time < end_time,
                    self.model.end_time >= end_time
                ),
                # Новая тренировка полностью покрывает существующую
                and_(
                    self.model.start_time >= start_time,
                    self.model.end_time <= end_time
                )
            )

            # Ищем конфликты по помещению ИЛИ тренеру одним запросом
            query = select(self.model).where(
                and_(
                    self.model.date == training_date,
                    or_(
                        self.model.room_id == room_id,
                        self.model.trainer_id == trainer_id
                    ),
                    time_overlap
                )
            )

            # Если редактируем существующую тренировку, исключаем её из проверки
            if exclude_training_id:
                query = query.where(self.model.id != exclude_training_id)

            result = await self._session.execute(query)
            conflicting_trainings = result.scalars().all()

            if not conflicting_trainings:
                logger.info("Конфликтов не обнаружено")
                return False, None

            # Проверяем приоритет конфликтов: сначала помещение, потом тренер
            for training in conflicting_trainings:
                if training.room_id == room_id:
                    logger.warning(
                        f"Конфликт помещения: тренировка '{training.title}' "
                        f"уже занимает помещение {room_id} на {training_date} "
                        f"с {training.start_time} до {training.end_time}"
                    )
                    return True, "room"

            # Если конфликта по помещению нет, проверяем тренера
            for training in conflicting_trainings:
                if training.trainer_id == trainer_id:
                    logger.warning(
                        f"Конфликт тренера: тренер {trainer_id} уже ведет тренировку '{training.title}' "
                        f"на {training_date} с {training.start_time} до {training.end_time}"
                    )
                    return True, "trainer"

            # Не должны сюда попасть, но на всякий случай
            logger.info("Конфликтов не обнаружено")
            return False, None

        except Exception as e:
            logger.error(f"Ошибка при проверке конфликтов: {e}")
            raise
