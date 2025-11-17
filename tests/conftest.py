import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.dao.database import Base
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.users.dao import UsersDAO
from app.users.schemas import SUserAddDB
from app.users.auth import get_password_hash
from app.users.models import Role

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

