from sqlalchemy import (String, Integer, Column,
    MetaData, ForeignKey, Table, FLOAT)

from auth.models import user

metadata_restoraunt = MetaData()

#Модель меню 
MenuModel = Table(
    'menu',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),

    Column('restoraunt_id', Integer, ForeignKey('restorunt.id', name="fk_menu_restoraunt"), nullable=False, unique=True)
)

#Модель ресторана
Restoraunt = Table(
    'restorunt',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False, unique=True),
    Column('rating', FLOAT, default=0.0), 
    Column('address', String),
    Column('description', String, nullable=True),

    #ССылка на пользователя, который оформил размещение ресторана
    Column('user_id', Integer, ForeignKey(user.c.id, name="fk_restoraunt_user"), nullable=False),
    Column('menu_id', Integer, ForeignKey(MenuModel.c.id, name="fk_restorunt_menu"), nullable=True)
)

#Модель контакной информации
ContactModel = Table(
    'contact',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('phone', String, nullable=False),
    Column('manager', String, nullable=True),
    Column('office_restoraunt_address', String, nullable=True),

    #К какому ресторану будет относится эта схема
    Column('restoraunt_id', Integer, ForeignKey(Restoraunt.c.id, name="fk_contact_restoraunt"), nullable=False, unique=True)
)

#Модель категорий
CategoryModel = Table(
    'category',
    metadata_restoraunt,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),

    Column('menu_id', Integer, ForeignKey(MenuModel.c.id, name="fk_category_menu"), nullable=False),
    Column('restoraunt_id', Integer, ForeignKey(Restoraunt.c.id, name="fk_category_restoraunt"), nullable=False)
)

#Модель блюд
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
    Column('category_id', Integer, ForeignKey(CategoryModel.c.id, name="fk_dishes_category"), nullable=False),
    Column('menu_id', Integer, ForeignKey(MenuModel.c.id, name="fk_dishes_menu"),nullable=False),
    Column('restoraunt_id', Integer, ForeignKey(Restoraunt.c.id, name="fk_dishes_restorunt"), nullable=False),
)