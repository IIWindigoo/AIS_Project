import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import select
from httpx import AsyncClient, ASGITransport
from datetime import date, time

from app.main import app
from app.dao.database import Base
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.users.dao import UsersDAO
from app.users.schemas import SUserAddDB
from app.users.auth import get_password_hash
from app.users.models import Role, User
from app.rooms.models import Room
from app.trainings.models import Training

# Тестовая база данных 
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

    # Удаляем таблицы после теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def roles_fixture(db_session):
    roles = [
        Role(name="client"),
        Role(name="trainer"),
        Role(name="admin"),
    ]
    db_session.add_all(roles)
    await db_session.commit()
    
    stored = (await db_session.execute(select(Role))).scalars().all()
    return {r.name: r for r in stored}
    

@pytest_asyncio.fixture
async def trainer_fixture(db_session, roles_fixture):
    trainer_role = roles_fixture["trainer"]
    trainer = User(
        phone_number="+79999999999",
        first_name="Trainer",
        last_name="Trainer",
        email="trainer@example.com",
        password=get_password_hash("12345"),
        role_id=trainer_role.id,
    )
    db_session.add(trainer)
    await db_session.commit()
    await db_session.refresh(trainer)
    return trainer

@pytest_asyncio.fixture
async def client_fixture(db_session, roles_fixture):
    client_role = roles_fixture["client"]
    client = User(
        phone_number="+78888888888",
        first_name="Client",
        last_name="Client",
        email="client@example.com",
        password=get_password_hash("12345"),
        role_id=client_role.id,
    )
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    return client

@pytest_asyncio.fixture
async def room_fixture(db_session):
    room = Room(
        title="Большой зал",
        capacity=20
    )
    db_session.add(room)
    await db_session.commit()
    await db_session.refresh(room)
    return room

@pytest_asyncio.fixture
async def training_fixture(db_session, trainer_fixture, room_fixture):
    training = Training(
        title="Кардио",
        description="Описание",
        date=date.today(),
        start_time=time(15, 0),
        end_time=time(16, 0),
        trainer_id=trainer_fixture.id,
        room_id=room_fixture.id,
    )
    db_session.add(training)
    await db_session.commit()
    await db_session.refresh(training)
    return training


"""
@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    # Переопределяем зависимости
    async def override_get_session_without_commit():
        return db_session
    
    async def override_get_session_with_commit():
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise
    
    app.dependency_overrides[get_session_without_commit] = override_get_session_without_commit
    app.dependency_overrides[get_session_with_commit] = override_get_session_with_commit

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def training_data():
    return {
        "title": "Утренняя йога",
        "description": "Расслабляющая тренировка для начинающих",
        "date": "2024-01-15",
        "start_time": "09:00:00",
        "end_time": "10:00:00"
    }

# @pytest_asyncio.fixture
# async def default_roles(db_session):
#     # создаём роли
#     client_role = Role(id=1, name="client")
#     trainer_role = Role(id=2, name="trainer")
#     admin_role = Role(id=3, name="admin")

#     db_session.add_all([client_role, trainer_role, admin_role])
#     await db_session.commit()
#     return {"client": client_role, "trainer": trainer_role, "admin": admin_role}

@pytest_asyncio.fixture
async def default_roles(db_session):
    role = Role(name="client")
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role

@pytest_asyncio.fixture
async def test_user(db_session, default_roles):
    dao = UsersDAO(db_session)
    user = SUserAddDB(
        email="test@example.com",
        phone_number="+79991234567",
        first_name="Test",
        last_name="User",
        password=get_password_hash("12345")
    )
    await dao.add(values=user)
    return user

"""