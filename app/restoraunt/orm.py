from .models import Restoraunt, MenuModel, CategoryModel,DishesModel,ContactModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import AddDishiesSchema




async def create_restoraunt_orm(*, title,rating,address,description, user_id, session):
    query = insert(Restoraunt).values(title=title,rating=rating,address=address,description=description,user_id=user_id)
    await session.execute(query)
    await session.commit()


async def get_info_restoraunt_by_id(*, restoraunt_id,session):
    query = select(Restoraunt).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
    #mappings() - вернет dict с объектами типа ключ значение из базы
    return result.mappings().all()


async def get_restoraunt_osnov_for_id_rest(*, session: AsyncSession,restoraunt_id:int):
    query = select(Restoraunt.c.user_id).where(Restoraunt.c.id == restoraunt_id)
    user_id = await session.execute(query)
    return user_id.scalars().all()


async def add_new_info_for_menu(*, restoraunt_id:int, session: AsyncSession, title, description):
    query = insert(MenuModel).values(title=title, description=description, restoraunt_id=restoraunt_id).returning(MenuModel)
    
    result = await session.execute(query)
    menu_id_after_adds = result.first()[0]
    query1 = update(Restoraunt).values(menu_id=menu_id_after_adds).where(Restoraunt.c.id == restoraunt_id)
    await session.execute(query1)
    await session.commit()




async def get_info_for_menu_restoraunt(*, restoraunt_id,session):
    query = select(MenuModel.c.id).where(MenuModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    return result.first()

async def add_new_category_for_menu(*, menu_id, title,description, session,restoraunt_id):
    query = insert(CategoryModel).values(title=title,description=description,menu_id=menu_id,restoraunt_id=restoraunt_id)
    await session.execute(query)
    await session.commit()


async def get_category_for_menu(*, menu_id, session):
    query = select(CategoryModel.c.id).where(CategoryModel.c.menu_id == menu_id)
    result = await session.execute(query)
    return result.scalars().all()

async def add_new_dishaes_on_category(*, list_of_dishies: List[AddDishiesSchema],session,category_id, restoraunt_id,menu_id):
    for dishies in list_of_dishies:
        query = insert(DishesModel).values(**dishies.model_dump(), category_id=category_id,restoraunt_id=restoraunt_id,menu_id=menu_id)
        await session.execute(query)
    await session.commit()


async def get_contact_info(*,session,restoraunt_id):
    query = select(ContactModel).where(ContactModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    return result.mappings().all()

async def add_new_contact_info_for_restorant(*,session,restoraunt_id, phone,manager,office_restoraunt_address):
    query = insert(ContactModel).values(restoraunt_id=restoraunt_id,phone=phone,manager=manager,office_restoraunt_address=office_restoraunt_address)
    await session.execute(query)
    await session.commit()


async def get_restaraunt_menu(*, session, restoraunt_id):
    query = select(Restoraunt.c.menu_id).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
    return result.first()

async def get_category_orm(*, session, restoraunt_id):
    query = select(CategoryModel).where(CategoryModel.c.menu_id == restoraunt_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_list_products_for_category(*, session, category_id):
    query = select(DishesModel).where(DishesModel.c.category_id == category_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_menu_info_for_orm(*, session, restoraunt_id):
    query = select(MenuModel).where(MenuModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    #if result.mappings().all():
    return result.mappings().all()
    #else:
    #    return {}

async def get_list_title_restoraunt(*, session):
    query = select(Restoraunt.c.title)
    result = await session.execute(query)
    return result.scalars().all()


async def get_menu_id_for_restoraunt(*, session, restoraunt_id):
    query = select(Restoraunt.c.menu_id).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
    return result.all()