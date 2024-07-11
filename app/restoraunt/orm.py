from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .models import Restoraunt, MenuModel, CategoryModel,DishesModel,ContactModel
from .schemas import AddDishiesSchema




async def create_restoraunt_orm(*, title,rating,address,description, user_id, session:AsyncSession):
    query = insert(Restoraunt).values(
    title=title,
    rating=rating,
    address=address,
    description=description,
    user_id=user_id
    )
    await session.execute(query)
    await session.commit()


async def get_info_restoraunt_by_id(*, restoraunt_id:int,session: AsyncSession):
    query = select(Restoraunt).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
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

async def add_new_category_for_menu(*, menu_id, title,description, session:AsyncSession,restoraunt_id:int):
    query = insert(CategoryModel).values(title=title,description=description,menu_id=menu_id,restoraunt_id=restoraunt_id)
    await session.execute(query)
    await session.commit()

async def get_category_for_menu(*, menu_id:int, session:AsyncSession):
    query = select(CategoryModel.c.id).where(CategoryModel.c.menu_id == menu_id)
    result = await session.execute(query)
    return result.scalars().all()

async def add_new_dishaes_on_category(*, 
    list_of_dishies: List[AddDishiesSchema],
    session:AsyncSession,
    category_id:int, 
    restoraunt_id:int,
    menu_id:int
):
    for dishies in list_of_dishies:
        query = insert(DishesModel).values(
        **dishies.model_dump(), category_id=category_id,restoraunt_id=restoraunt_id,menu_id=menu_id
        )
        await session.execute(query)
    await session.commit()

async def get_contact_info_orm(*,session:AsyncSession,restoraunt_id:int):
    query = select(ContactModel).where(ContactModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    return result.mappings().all()

async def add_new_contact_info_for_restorant(*,session:AsyncSession,restoraunt_id:int, phone,manager,office_restoraunt_address):
    query = insert(ContactModel).values(
        restoraunt_id=restoraunt_id,
        phone=phone,
        manager=manager,
        office_restoraunt_address=office_restoraunt_address
        )
    await session.execute(query)
    await session.commit()

async def get_restaraunt_menu(*, session:AsyncSession, restoraunt_id:int):
    query = select(Restoraunt.c.menu_id).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
    return result.first()

async def get_category_orm(*, session:AsyncSession, restoraunt_id:int):
    query = select(CategoryModel).where(CategoryModel.c.menu_id == restoraunt_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_list_products_for_category(*, session:AsyncSession, category_id:int):
    query = select(DishesModel).where(DishesModel.c.category_id == category_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_menu_info_for_orm(*, session:AsyncSession, restoraunt_id:int):
    query = select(MenuModel).where(MenuModel.c.restoraunt_id == restoraunt_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_list_title_restoraunt(*, session:AsyncSession):
    query = select(Restoraunt.c.title)
    result = await session.execute(query)
    return result.scalars().all()

async def get_menu_id_for_restoraunt(*, session:AsyncSession, restoraunt_id:int):
    query = select(Restoraunt.c.menu_id).where(Restoraunt.c.id == restoraunt_id)
    result = await session.execute(query)
    return result.all()

async def get_info_for_restoraunt_orm(*, session:AsyncSession, title_rest):
    query = select(Restoraunt.c.id).where(Restoraunt.c.title == title_rest)
    result = await session.execute(query)
    return result.first()