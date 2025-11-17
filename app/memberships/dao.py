from app.dao.base import BaseDAO
from app.memberships.models import Membership, SubRequest


class MembershipDAO(BaseDAO):
    model = Membership

class SubRequestDAO(BaseDAO):
    model = SubRequest