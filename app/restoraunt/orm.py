from .models import Restoraunt, MenuModel, CategoryModel,DishesModel
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
    return user_id.one()


async def add_new_info_for_menu(*, restoraunt_id:int, session: AsyncSession, title, description):
    query = insert(MenuModel).values(title=title, description=description, restoraunt_id=restoraunt_id)
    await session.execute(query)
    await session.commit()



async def get_info_for_menu_restoraunt(*, restoraunt_id,session):
    query = select(MenuModel.c.id).where(MenuModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    return result.first()

async def add_new_category_for_menu(*, menu_id, title,description, session):
    query = insert(CategoryModel).values(title=title,description=description,menu_id=menu_id)
    await session.execute(query)
    await session.commit()


async def get_category_for_menu(*, menu_id,restoraunt_id,category_id, session):
    query = select(CategoryModel.c.menu_id).where(CategoryModel.c.menu_id == menu_id)
    result = await session.execute(query)
    return result.all()

async def add_new_dishaes_on_category(*, list_of_dishies: List[AddDishiesSchema],session,category_id):
    for dishies in list_of_dishies:
        query = insert(DishesModel).values(**dishies.model_dump(), category_id=category_id)
        await session.execute(query)
    await session.commit()
