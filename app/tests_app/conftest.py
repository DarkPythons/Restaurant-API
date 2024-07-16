import asyncio
from fastapi.testclient import TestClient
import pytest, pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from typing import AsyncGenerator

from config import TestingAppDatabaseSettings
from database import METADATA_TABLE_LIST, get_async_session, METADATA_TABLE_LIST_FOR_DELETE
from main import app
from auth.models import Bases_meta

settings_testDb = TestingAppDatabaseSettings()
database_url_test = f"postgresql+asyncpg://\
{settings_testDb.DB_USER_TEST}:{settings_testDb.DB_PASS_TEST}@\
{settings_testDb.DB_HOST_TEST}:{settings_testDb.DB_PORT_TEST}/\
{settings_testDb.DB_NAME_TEST}"

engine_test = create_async_engine(database_url_test, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

#Переназначение метаданных на тестовый движок тестовой базы данных
for one_metadata in METADATA_TABLE_LIST:
    one_metadata.bind = engine_test
#Bases_meta.metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

#Переключение зависимости подключения к базе на тестовое
app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture(autouse=True, scope="session")
async def create_delete_table_in_db():
    #Перед тестами
    async with engine_test.begin() as connect:
        await connect.run_sync(Bases_meta.metadata.create_all)
        for one_metadata in METADATA_TABLE_LIST:
            await connect.run_sync(one_metadata.create_all)
    yield
    #После тестов
    async with engine_test.begin() as connect:
        for one_metadata in METADATA_TABLE_LIST_FOR_DELETE:
            await connect.run_sync(one_metadata.drop_all)
        await connect.run_sync(Bases_meta.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()

#Синхронное взаимодействие
client = TestClient(app)

#Асинхронное взаимодействие
@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac