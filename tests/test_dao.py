import pytest
from datetime import date, timedelta
from pydantic import BaseModel

from app.trainings.dao import TrainingDAO
from app.trainings.schemas import STrainingAdd, STrainingUpd, STrainingFilter
from app.rooms.dao import RoomDAO
from app.rooms.schemas import SRoomAdd, SRoomFilter, SRoomUpd
from app.subscriptions.dao import SubscriptionDAO
from app.subscriptions.schemas import SSubAdd, SSubFilter, SSubUpd
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingAddFull
from app.memberships.dao import SubRequestDAO, MembershipDAO
from app.memberships.schemas import (SSubReqAdd, SSubReqUpdate, SSubReqFilter, SMembershipCreate,
                                     SMembershipInfo, SMembershipUpd, SMembershipFilter)
from app.users.dao import UsersDAO
from app.users.schemas import SUserAddDB
from app.users.auth import get_password_hash

@pytest.mark.asyncio
class TestTrainingDAO:
    
    @pytest.fixture
    def dao(self, db_session) -> TrainingDAO:
        return TrainingDAO(db_session)
    
    @pytest.fixture
    def sample_training_data(self, trainer_fixture, room_fixture):
        return STrainingAdd(
            title="Йога",
            description="Описание",
            date=str(date.today()),
            start_time="15:00",
            end_time="16:00",
            trainer_id=trainer_fixture.id,
            room_id=room_fixture.id,
        )

    async def test_create_training(self, dao, sample_training_data, trainer_fixture):
        new_training = await dao.add(sample_training_data)
        assert new_training.id is not None
        assert new_training.title == "Йога"
        assert new_training.trainer_id == trainer_fixture.id
    
    async def test_training(self, dao, sample_training_data):
        new_training = await dao.add(sample_training_data)
        found = await dao.find_one_or_none_by_id(new_training.id)
        print(found)
        assert found is not None
        assert found.title == "Йога"
        update_count = await dao.update(
            STrainingFilter(id=new_training.id),
            STrainingUpd(title="Нога"),
        )
        updated_training = await dao.find_one_or_none_by_id(new_training.id)
        assert updated_training.title == "Нога"
        print(updated_training)
        delete = await dao.delete(STrainingFilter(id=updated_training.id))
        assert delete == 1
        assert await dao.find_one_or_none_by_id(updated_training.id) is None

    async def test_update_training(self, dao, sample_training_data):
        new_training = await dao.add(sample_training_data)
        update_count = await dao.update(
            STrainingFilter(id=new_training.id),
            STrainingUpd(title="Новое название"),
        )
        assert update_count == 1
        updated_training = await dao.find_one_or_none_by_id(new_training.id)
        assert updated_training.title == "Новое название"
    
    async def test_delete_training(self, dao, sample_training_data):
        new_training = await dao.add(sample_training_data)
        deleted_count = await dao.delete(STrainingFilter(id=new_training.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(new_training.id) is None

@pytest.mark.asyncio
class TestRoomDAO:
    @pytest.fixture
    def dao(self, db_session) -> RoomDAO:
        return RoomDAO(db_session)
    
    @pytest.fixture
    def room_data(self):
        return SRoomAdd(
            title="Зал",
            capacity=20,
        )
    
    async def test_room(self, dao, room_data):
        room = await dao.add(room_data)
        found = await dao.find_one_or_none_by_id(room.id)
        print(found)
        assert found is not None
        assert found.title == "Зал"
        updated_count = await dao.update(
            SRoomFilter(id=room.id),
            SRoomUpd(capacity=33),
        )
        updated_room = await dao.find_one_or_none_by_id(room.id)
        print(updated_room)
        assert updated_count == 1
        assert updated_room.capacity == 33
        deleted_count = await dao.delete(SRoomFilter(id=updated_room.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(updated_room.id) is None

    async def test_create_room(self, dao, room_data):
        room = await dao.add(room_data)
        assert room.id is not None
        assert room.title == "Зал"
    
    async def test_find_room(self, dao, room_data):
        room = await dao.add(room_data)
        found = await dao.find_one_or_none_by_id(room.id)
        assert found is not None
        assert found.title == "Зал"
    
    async def test_update_room(self, dao, room_data):
        room = await dao.add(room_data)
        updated_count = await dao.update(
            SRoomFilter(id=room.id),
            SRoomUpd(capacity=33),
        )
        updated_room = await dao.find_one_or_none_by_id(room.id)
        assert updated_count == 1
        assert updated_room.capacity == 33
    
    async def test_delete_room(self, dao, room_data):
        room = await dao.add(room_data)
        deleted_count = await dao.delete(SRoomFilter(id=room.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(room.id) is None

@pytest.mark.asyncio
class TestSubscriptionDAO:
    @pytest.fixture
    def dao(self, db_session) -> SubscriptionDAO:
        return SubscriptionDAO(db_session)
    
    @pytest.fixture
    def sub_data(self):
        return SSubAdd(
            title="Годовой",
            price=15000,
            duration_days=365,
        )
    async def test_sub(self, dao, sub_data):
        sub = await dao.add(sub_data)
        found = await dao.find_one_or_none_by_id(sub.id)
        print(found)
        assert sub.id is not None
        assert sub.title == "Годовой"
        updated_count = await dao.update(
            SSubFilter(id=sub.id),
            SSubUpd(price=20000),
        )
        updated_sub = await dao.find_one_or_none_by_id(sub.id)
        print(updated_sub)
        assert updated_count == 1
        assert updated_sub.price == 20000
        deleted_count = await dao.delete(SSubFilter(id=sub.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(sub.id) is None

    async def test_create_sub(self, dao, sub_data):
        sub = await dao.add(sub_data)
        assert sub.id is not None
        assert sub.title == "Годовой"
    
    async def test_find_sub(self, dao, sub_data):
        sub = await dao.add(sub_data)
        found = await dao.find_one_or_none_by_id(sub.id)
        assert found is not None
        assert found.title == "Годовой"
    
    async def test_update_sub(self, dao, sub_data):
        sub = await dao.add(sub_data)
        updated_count = await dao.update(
            SSubFilter(id=sub.id),
            SSubUpd(price=20000),
        )
        updated_sub = await dao.find_one_or_none_by_id(sub.id)
        assert updated_count == 1
        assert updated_sub.price == 20000
    
    async def test_delete_sub(self, dao, sub_data):
        sub = await dao.add(sub_data)
        deleted_count = await dao.delete(SSubFilter(id=sub.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(sub.id) is None

@pytest.mark.asyncio
class TestBookingDAO:
    @pytest.fixture
    def dao(self, db_session) -> BookingDAO:
        return BookingDAO(db_session)
    
    @pytest.fixture
    def booking_data(self, client_fixture, training_fixture):
        return SBookingAddFull(
            training_id=training_fixture.id,
            user_id=client_fixture.id,
        )
    
    async def test_booking(self, dao, booking_data, client_fixture, training_fixture):
        booking = await dao.add(booking_data)
        assert booking.id is not None
        assert booking.training_id == training_fixture.id
        assert booking.user_id == client_fixture.id
        bookings_of_user = await dao.find_by_user(client_fixture.id)
        print(bookings_of_user)
        assert len(bookings_of_user) == 1
        found = bookings_of_user[0]
        assert found.id == booking.id
        assert found.user_id == client_fixture.id
        deleted_count = await dao.delete(
            SBookingAddFull(
                user_id=found.user_id, 
                training_id=found.training_id,
                )
            )
        assert deleted_count == 1
    
@pytest.mark.asyncio
class TestSubRequestDAO:
    @pytest.fixture
    def dao(self, db_session) -> SubRequestDAO:
        return SubRequestDAO(db_session)
    
    @pytest.fixture
    def subrequest_data(self, subscription_fixture, client_fixture):
        return SSubReqAdd(
            user_id=client_fixture.id,
            subscription_id=subscription_fixture.id
        )
    
    async def test_sub_request(self, dao, subrequest_data):
        sub_request = await dao.add(subrequest_data)
        found = await dao.find_requests_with_data()
        print(found)
        assert sub_request.id is not None
        assert sub_request.user_id == 1
        updated_count = await dao.update(
            SSubReqFilter(id=sub_request.id),
            SSubReqUpdate(status="approved")
        )
        updated_sub_request = await dao.find_one_or_none_by_id(sub_request.id)
        print(updated_sub_request)
        assert updated_count == 1
        assert updated_sub_request.status == "approved"

@pytest.mark.asyncio
class TestMembershipDAO:
    @pytest.fixture
    def dao(self, db_session) -> MembershipDAO:
        return MembershipDAO(db_session)
    
    @pytest.fixture
    def membership_data(self, subscription_fixture, client_fixture):
        start_date = date.today()
        end_date = start_date + timedelta(days=subscription_fixture.duration_days)
        return SMembershipCreate(
            user_id=client_fixture.id,
            subscription_id=subscription_fixture.id,
            start_date = start_date,
            end_date = end_date,
            status="active",
        )

    async def test_membership(self, dao, membership_data, client_fixture):
        membership = await dao.add(membership_data)
        found = await dao.find_one_or_none_by_id(membership.id)
        print(found)
        assert membership.id is not None
        updated_count = await dao.update(
            SMembershipFilter(user_id=client_fixture.id),
            SMembershipUpd(status="inactive")
        )
        updated_membership = await dao.find_one_or_none(SMembershipFilter(user_id=client_fixture.id))
        print(updated_membership)
        assert updated_count == 1
        assert updated_membership.status == "inactive"

class SUserFilter(BaseModel):
    id: int

@pytest.mark.asyncio
class TestUserDAO:
    @pytest.fixture
    def dao(self, db_session) -> UsersDAO:
        return UsersDAO(db_session)
    
    @pytest.fixture
    def user_data(self):
        return SUserAddDB(
            phone_number="+71234567890",
            first_name="Client2",
            last_name="Client2",
            email="client2@example.com",
            password=get_password_hash("12345"),
        )
    
    async def test_user(self, dao, user_data, client_fixture):
        user = await dao.add(user_data)
        found = await dao.find_all()
        print(found)
        assert user.id is not None
        assert user.email == "client2@example.com"
        deleted_count = await dao.delete(SUserFilter(id=user.id))
        assert deleted_count == 1
        assert await dao.find_one_or_none_by_id(user.id) is None
        found = await dao.find_all()
        print(found)