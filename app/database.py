from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends 
from typing import Annotated

from config import DataBaseSettingPostgre
from auth.models import Bases_meta, metadata_for_table2_user, User
from restoraunt.models import metadata_restoraunt
from courier.models import courier_metadata
from backet.models import backet_metadata
from orders.models import orders_metadata

database_settings = DataBaseSettingPostgre()

#url базы данных
DATABASE_URL = f"postgresql+asyncpg://\
{database_settings.DB_USER}:{database_settings.DB_PASS}@\
{database_settings.DB_HOST}:{database_settings.DB_PORT}/\
{database_settings.DB_NAME}"


#Создание движка
engine = create_async_engine(DATABASE_URL)

#Шаблон подключения для сессии
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



METADATA_TABLE_LIST = [
    metadata_for_table2_user,
    metadata_restoraunt,
    courier_metadata,
    orders_metadata,
    backet_metadata,
]

METADATA_TABLE_LIST_FOR_DELETE = [
    backet_metadata,
    orders_metadata,
    courier_metadata,
    metadata_restoraunt,
    metadata_for_table2_user
]

async def create_table():
    async with engine.begin() as connect:
        #Создаение всех таблиц
        await connect.run_sync(Bases_meta.metadata.create_all)
        for metadata in METADATA_TABLE_LIST:
            await connect.run_sync(metadata.create_all)



async def delete_table():
    async with engine.begin() as connect:
        #Удаление всех таблиц (При удалении идёт другой порядок, чтобы внешнии ключи не вызывали ошибки)
        for metadata in METADATA_TABLE_LIST_FOR_DELETE:
            await connect.run_sync(metadata.drop_all)
        await connect.run_sync(Bases_meta.metadata.drop_all)
        


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

#Получение юзера из базы
async def get_user_db(session: Annotated[AsyncSession, Depends(get_async_session)]):
    yield SQLAlchemyUserDatabase(session, User)

