import pytest
from datetime import date

from app.trainings.dao import TrainingDAO
from app.trainings.schemas import STrainingAdd, STrainingUpd, STrainingFilter
from app.rooms.dao import RoomDAO
from app.rooms.schemas import SRoomAdd, SRoomFilter, SRoomUpd
from app.subscriptions.dao import SubscriptionDAO
from app.subscriptions.schemas import SSubAdd, SSubFilter, SSubUpd
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingAddFull


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
    
    async def test_find_training(self, dao, sample_training_data):
        new_training = await dao.add(sample_training_data)
        found = await dao.find_one_or_none_by_id(new_training.id)
        assert found is not None
        assert found.title == "Йога"

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
    
    async def test_add_booking(self, dao, booking_data, client_fixture, training_fixture):
        booking = await dao.add(booking_data)
        assert booking.id is not None
        assert booking.training_id == training_fixture.id
        assert booking.user_id == client_fixture.id