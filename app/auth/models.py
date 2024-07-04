from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String,Boolean, MetaData, Column, Table
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated



metadata_for_table2_user = MetaData()
Bases_meta: DeclarativeMeta = declarative_base()

#Модель для первичной регитрации пользователя
class User(SQLAlchemyBaseUserTable[int], Bases_meta):
    __tablename__ = 'user'

    #Переопределние колонок из SQLAlchemyBaseUserTable
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,  default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)



user = Table(
    'user',
    metadata_for_table2_user,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)