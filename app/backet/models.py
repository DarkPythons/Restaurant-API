from sqlalchemy import (Integer, Column,
    MetaData, ForeignKey, Table)

from auth.models import user
from restoraunt.models import DishesModel
from orders.models import OrderTable

backet_metadata = MetaData()

BacketTable = Table(
    'backet',
    backet_metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey(user.c.id, ondelete='RESTRICT'), nullable=False),
    Column('item_id', ForeignKey(DishesModel.c.id, ondelete='RESTRICT'), nullable=False),
    Column('order_id', ForeignKey(OrderTable.c.id, ondelete='SET NULL'), nullable=True),
)
