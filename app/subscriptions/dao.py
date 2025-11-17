from app.dao.base import BaseDAO
from app.subscriptions.models import Subscription


class SubscriptionDAO(BaseDAO):
    model = Subscription