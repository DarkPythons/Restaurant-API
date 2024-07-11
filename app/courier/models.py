from sqlalchemy import (String, Integer, Column,
    Boolean, MetaData, ForeignKey, Table)
from auth.models import user

courier_metadata = MetaData()



CourierTable = Table(
    'courier',
    courier_metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False, unique=True),
    Column('first_name', String(length=50), nullable=False),
    Column('last_name', String(length=50), nullable=False),
    Column('phone', String(length=20), nullable=False),
    Column('verified', Boolean, nullable=False),
    Column('in_work', Boolean, nullable=False),

    Column('user_id', Integer, ForeignKey(user.c.id, ondelete='RESTRICT'), nullable=False),
)