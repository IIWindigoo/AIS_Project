from app.dao.base import BaseDAO
from app.memberships.models import Membership, SubRequest

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger


class MembershipDAO(BaseDAO):
    model = Membership

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