from sqlalchemy import (String, Integer, TIMESTAMP, Column,
    Boolean, MetaData, ForeignKey, Table, FLOAT)
from auth.models import user



metadata_restoraunt = MetaData()







#Модель создания ресторана
Restoraunt = Table(
    'restorunt',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False, unique=True),
    Column('rating', FLOAT, default=0.0), 
    Column('address', String),
    Column('description', String, nullable=True),

    #ССылка на пользователя, который оформил размещение ресторана
    Column('user_id', Integer, ForeignKey(user.c.id, ondelete='RESTRICT'), nullable=False)
)



MenuModel = Table(
    'menu',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),
    Column('restoraunt_id', Integer, ForeignKey(Restoraunt.c.id, ondelete='RESTRICT'), nullable=False)
)

ContactModel = Table(
    'contact',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('phone', String),
    Column('manager', String, nullable=True),
    Column('office_restoraunt_address', String, nullable=True),

    #К какому ресторану будет относится эта схема
    Column('restoraunt_id', Integer, ForeignKey(Restoraunt.c.id, ondelete='RESTRICT'), nullable=False)
)




CategoryModel = Table(
    'category',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),

    Column('menu_id', Integer, ForeignKey(MenuModel.c.id, ondelete='RESTRICT'), nullable=False)
)




DishesModel = Table(
    'dishes',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),
    Column('price', Integer, nullable=False),
    Column('sostav', String, nullable=False),
    Column('kolories', Integer, nullable=True),

    #Ссылка к какой категории относится блюдо
    Column('category_id', ForeignKey(CategoryModel.c.id, ondelete='RESTRICT'), nullable=False)
)