from sqlalchemy import (String, Integer, TIMESTAMP, Column,
    Boolean, MetaData, ForeignKey, Table, FLOAT,DateTime)
from auth.models import user
from sqlalchemy.sql import func
from restoraunt.models import DishesModel

backet_metadata = MetaData()

BacketTable = Table(
    'backet',
    backet_metadata,

    Column('id', Integer, primary_key=True),
    Column('in_order', Boolean, nullable=False),
    #Кому запись в backet принадлжеит 
    Column('user_id', ForeignKey(user.c.id, ondelete='RESTRICT'), nullable=False),
    #Предмет который человек добавил
    Column('item_id', ForeignKey(DishesModel.c.id, ondelete='RESTRICT'), nullable=False)

)