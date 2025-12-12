from app.dao.base import BaseDAO
from app.memberships.models import Membership, SubRequest

from sqlalchemy import select, and_, update
from sqlalchemy.orm import selectinload
from loguru import logger
from datetime import date


class MembershipDAO(BaseDAO):
    model = Membership

    async def find_memberships_with_data(self):
        logger.info("Поиск действующих абонементов с загрузкой user и subscription")
        try:
            query = (
                select(self.model)
                .options(
                    selectinload(self.model.user),
                    selectinload(self.model.subscription)
                )
            )
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} действующих абонементов.")
            return records
        except Exception as e:
            logger.error(f"Ошибка при поиске действующих абонементов: {e}")
            raise

    async def deactivate_expired_memberships(self) -> int:
        """
        Деактивирует все абонементы, срок действия которых истек.
        Возвращает количество деактивированных абонементов.
        """
        logger.info("Проверка и деактивация истекших абонементов")
        try:
            today = date.today()

            # Находим все активные абонементы с истекшим сроком
            query = (
                update(self.model)
                .where(
                    and_(
                        self.model.status == "active",
                        self.model.end_date < today
                    )
                )
                .values(status="expired")
            )

            result = await self._session.execute(query)
            count = result.rowcount

            if count > 0:
                logger.info(f"Деактивировано {count} истекших абонементов")
            else:
                logger.info("Истекших абонементов не найдено")

            return count
        except Exception as e:
            logger.error(f"Ошибка при деактивации истекших абонементов: {e}")
            raise

class SubRequestDAO(BaseDAO):
    model = SubRequest

    async def find_requests_with_data(self):
        logger.info("Поиск всех заявок с загрузкой user и subscription")
        try:
            query = (
                select(self.model)
                .options(
                    selectinload(self.model.user),
                    selectinload(self.model.subscription)
                )
            )
            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} заявок.")
            return records
        except Exception as e:
            logger.error(f"Ошибка при поиске заявок: {e}")
            raise
