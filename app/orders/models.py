from sqlalchemy import (String, Integer, Column,
MetaData, ForeignKey, Table, FLOAT,DateTime)
from sqlalchemy.sql import func

from auth.models import user
from courier.models import CourierTable

orders_metadata = MetaData()



OrderTable = Table(
    'order',
    orders_metadata,
    Column('id', Integer, primary_key=True),
    Column('price_order', FLOAT, nullable=False),
    Column('status', String, nullable=False),
    Column('time_create', DateTime(timezone=True), server_default=func.now()),
    Column('address', String, nullable=False),
    Column('user_id', ForeignKey(user.c.id, name="fk_order_user"), nullable=False),
    Column('courier_id', ForeignKey(CourierTable.c.id, name="fk_order_courier"), nullable=True)

)