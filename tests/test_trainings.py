import pytest
import pytest_asyncio
from fastapi import status
from datetime import date

from app.trainings.dao import TrainingDAO
from app.users.dao import UsersDAO
from app.users.schemas import SUserAddDB
from app.users.auth import get_password_hash
from app.users.models import Role


# -------------------- FIXTURES --------------------


@pytest_asyncio.fixture
async def normal_user(db_session, default_roles):
    dao = UsersDAO(db_session)
    user = SUserAddDB(
        email="user@example.com",
        phone_number="+70009998877",
        first_name="Normal",
        last_name="User",
        password=get_password_hash("12345")
    )
    added_user = await dao.add(values=user)
    await db_session.commit()
    await db_session.refresh(added_user)
    return added_user


@pytest_asyncio.fixture
async def auth_normal_client(client, normal_user):
    resp = await client.post("/users/login/", json={
        "email": normal_user.email,
        "password": "12345"
    })
    client.cookies.set("user_access_token", resp.cookies.get("user_access_token"))
    client.cookies.set("user_refresh_token", resp.cookies.get("user_refresh_token"))
    return client


# -------------------- HELPER --------------------

async def create_training(client, trainer_id, title="Йога"):
    training_data = {
        "title": title,
        "description": "Описание тренировки",
        "date": str(date.today()),
        "start_time": "09:00:00",
        "end_time": "10:00:00",
        "trainer_id": trainer_id,
    }
    resp = await client.post("/trainings/", json=training_data)
    assert resp.status_code == status.HTTP_200_OK, resp.text
    return resp.json()


# -------------------- TESTS --------------------

@pytest.mark.asyncio
class TestTrainingsCRUD:

    async def test_get_all_trainings_empty(self, client):
        resp = await client.get("/trainings/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []

    async def test_create_training_success(self, auth_trainer_client, trainer_user):
        training = await create_training(auth_trainer_client, trainer_user.id, "Утренняя йога")
        assert training["title"] == "Утренняя йога"
        assert training["trainer_id"] == trainer_user.id

    async def test_create_training_wrong_trainer(self, auth_trainer_client):
        training_data = {
            "title": "Вечерняя йога",
            "description": "Описание",
            "date": str(date.today()),
            "start_time": "18:00:00",
            "end_time": "19:00:00",
            "trainer_id": 9999
        }
        resp = await auth_trainer_client.post("/trainings/", json=training_data)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    async def test_create_training_unauthorized(self, client, trainer_user):
        training_data = {
            "title": "Неавторизованная йога",
            "description": "Описание",
            "date": str(date.today()),
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "trainer_id": trainer_user.id,
        }
        resp = await client.post("/trainings/", json=training_data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_training_success(self, auth_trainer_client, trainer_user, db_session):
        training = await create_training(auth_trainer_client, trainer_user.id, "Старая йога")
        training_id = training["id"]

        resp = await auth_trainer_client.patch(f"/trainings/{training_id}/", json={"title": "Новая йога"})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["title"] == "Новая йога"

        # Проверяем БД
        dao = TrainingDAO(db_session)
        updated = await dao.find_one_or_none_by_id(training_id)
        assert updated.title == "Новая йога"

    async def test_delete_training_success(self, auth_trainer_client, trainer_user, db_session):
        training = await create_training(auth_trainer_client, trainer_user.id, "Удалить меня")
        training_id = training["id"]

        resp = await auth_trainer_client.delete(f"/trainings/{training_id}/")
        assert resp.status_code == status.HTTP_200_OK
        assert "успешно удалена" in resp.json()["message"]

        dao = TrainingDAO(db_session)
        deleted = await dao.find_one_or_none_by_id(training_id)
        assert deleted is None

    async def test_forbidden_update_other_trainer(self, auth_trainer_client, db_session, default_roles):
        # Создаем другого тренера
        dao = UsersDAO(db_session)
        other_trainer = SUserAddDB(
            email="other@example.com",
            phone_number="+70001112244",
            first_name="Other",
            last_name="Trainer",
            password=get_password_hash("12345")
        )
        other_trainer_obj = await dao.add(values=other_trainer)
        await db_session.commit()
        await db_session.refresh(other_trainer_obj)

        # Создаем тренировку другого тренера
        training = await create_training(auth_trainer_client, other_trainer_obj.id, "Чужая йога")
        training_id = training["id"]

        resp = await auth_trainer_client.patch(f"/trainings/{training_id}/", json={"title": "Попытка"})
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_delete_other_trainer(self, auth_trainer_client, db_session, default_roles):
        # Создаем другого тренера
        dao = UsersDAO(db_session)
        other_trainer = SUserAddDB(
            email="other2@example.com",
            phone_number="+70001112255",
            first_name="Other2",
            last_name="Trainer",
            password=get_password_hash("12345")
        )
        other_trainer_obj = await dao.add(values=other_trainer)
        await db_session.commit()
        await db_session.refresh(other_trainer_obj)

        # Создаем тренировку другого тренера
        training = await create_training(auth_trainer_client, other_trainer_obj.id, "Чужая йога")
        training_id = training["id"]

        resp = await auth_trainer_client.delete(f"/trainings/{training_id}/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("payload,expected_status", [
        ({"title": "", "date": str(date.today()), "start_time": "09:00:00", "end_time": "10:00:00"}, 422),
        ({"title": "Йога", "date": "invalid-date", "start_time": "09:00:00", "end_time": "10:00:00"}, 422),
        ({"title": "Йога", "date": str(date.today()), "start_time": "10:00:00", "end_time": "09:00:00"}, 422),
    ])
    async def test_create_training_invalid_data(self, auth_trainer_client, trainer_user, payload, expected_status):
        payload["trainer_id"] = trainer_user.id
        resp = await auth_trainer_client.post("/trainings/", json=payload)
        assert resp.status_code == expected_status