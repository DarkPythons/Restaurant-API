from sqlalchemy import (String, Integer, TIMESTAMP, Column,
    Boolean, MetaData, ForeignKey, Table, FLOAT,DateTime)
from auth.models import user
from sqlalchemy.sql import func
import datetime

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

    #Кто создал заказ
    Column('user_id', ForeignKey(user.c.id, ondelete='RESTRICT'), nullable=False),
    #Айди доставляющего курьера (будет обновляться, когда курьер будет брать заказ по id)
    Column('courier_id', ForeignKey(CourierTable.c.id, ondelete='RESTRICT'), nullable=True)

)