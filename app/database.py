#Файл настройки базы данных
from config import DataBaseSettingPostgre, PROJECT_IS_PROCESS_DEBUG
from auth.models import Bases_meta, metadata_for_table2_user
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends 
from typing import Annotated
from auth.models import User
from restoraunt.models import metadata_restoraunt

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

async def create_table():
    async with engine.begin() as connect:
        #Создаение всех таблиц
        await connect.run_sync(Bases_meta.metadata.create_all)
        await connect.run_sync(metadata_for_table2_user.create_all)
        await connect.run_sync(metadata_restoraunt.create_all)

async def delete_table():
    async with engine.begin() as connect:
        #Удаление всех таблиц
        await connect.run_sync(Bases_meta.metadata.drop_all)
        await connect.run_sync(metadata_for_table2_user.drop_all)
        await connect.run_sync(metadata_restoraunt.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

#Получение юзера из базы
async def get_user_db(session: Annotated[AsyncSession, Depends(get_async_session)]):
    yield SQLAlchemyUserDatabase(session, User)

