from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String,Boolean, MetaData, Column, Table





metadata_for_table2_user = MetaData()
Bases_meta: DeclarativeMeta = declarative_base()

#Модель для первичной регитрации пользователя
class User(SQLAlchemyBaseUserTable[int], Bases_meta):
    __tablename__ = 'user'
    #Свои колонки
    first_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    phone: Mapped[str] = mapped_column(String(length=20), nullable=False)

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
    #Обязательные колонки
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),

    #Кастомные
    Column('first_name', String(length=50), nullable=False),
    Column('last_name', String(length=50), nullable=False),
    Column('phone', String(length=20), nullable=False)
)