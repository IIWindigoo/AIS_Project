import pytest
import pytest_asyncio
from fastapi import status
from sqlalchemy import select
from app.users.models import User


# --------- Фабрика данных ---------
def make_user_data(email="new@example.com"):
    return {
        "email": email,
        "phone_number": "+78881234567",
        "first_name": "New",
        "last_name": "User",
        "password": "12345",
        "confirm_password": "12345"
    }


@pytest.mark.asyncio
class TestRegister:
    async def test_register_new_user(self, client, db_session):
        user_data = make_user_data()
        resp = await client.post("/users/register/", json=user_data)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["message"] == "Вы успешно зарегистрированы!"

        # проверка побочного эффекта: юзер есть в базе
        result = await db_session.execute(select(User).filter_by(email=user_data["email"]))
        assert result.scalar_one_or_none() is not None

    async def test_register_user_already_exists(self, client, test_user):
        resp = await client.post("/users/register/", json=make_user_data(email="test@example.com"))
        assert resp.status_code == status.HTTP_409_CONFLICT

    async def test_register_with_invalid_email(self, client):
        resp = await client.post("/users/register/", json=make_user_data(email="not-an-email"))
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_register_with_mismatched_passwords(self, client):
        bad_data = make_user_data()
        bad_data["confirm_password"] = "wrong"
        resp = await client.post("/users/register/", json=bad_data)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, client, test_user):
        resp = await client.post("/users/login/", json={
            "email": "test@example.com",
            "password": "12345"
        })
        assert resp.status_code == status.HTTP_200_OK
        assert "user_access_token" in resp.cookies
        assert "user_refresh_token" in resp.cookies
        assert resp.json()["ok"] is True

    @pytest.mark.parametrize("password,status_code", [
        ("wrongpass", status.HTTP_401_UNAUTHORIZED),
        ("", status.HTTP_422_UNPROCESSABLE_ENTITY)
    ])
    async def test_login_failures(self, client, test_user, password, status_code):
        resp = await client.post("/users/login/", json={
            "email": "test@example.com",
            "password": password
        })
        assert resp.status_code == status_code


@pytest.mark.asyncio
class TestLogout:
    async def test_logout_success(self, client, test_user):
        # логинимся
        await client.post("/users/login/", json={"email": "test@example.com", "password": "12345"})
        resp = await client.post("/users/logout")

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["message"] == "Пользователь успешно вышел из системы"
        assert "user_access_token" not in resp.cookies or resp.cookies.get("user_access_token") == ""

@pytest_asyncio.fixture
async def auth_client(client, test_user):
    resp = await client.post("/users/login/", json={
        "email": "test@example.com",
        "password": "12345"
    })
    # вручную положим токены
    client.cookies.set("user_access_token", resp.cookies.get("user_access_token"))
    client.cookies.set("user_refresh_token", resp.cookies.get("user_refresh_token"))
    return client

@pytest.mark.asyncio
class TestGetMe:
    async def test_get_me_success(self, auth_client):
        resp = await auth_client.get("/users/me/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["email"] == "test@example.com"

    async def test_get_me_unauthorized(self, client):
        resp = await client.get("/users/me/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED