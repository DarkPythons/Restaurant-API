from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BacketTable
from restoraunt.models import DishesModel

async def get_info_for_orm(*, session:AsyncSession, item_id:int):
    query = select(DishesModel).where(DishesModel.c.id == item_id)
    result = await session.execute(query)
    return result.mappings().all()

async def add_new_item_for_backet_orm(*,session: AsyncSession, order_id:int, user_id:int, item_id:int):
    query = insert(BacketTable).values(user_id=user_id,order_id=order_id, item_id=item_id)
    await session.execute(query)
    await session.commit()

async def get_list_id_items(*, session: AsyncSession):
    query = select(DishesModel.c.id)
    result = await session.execute(query)
    return result.scalars().all()

async def get_raw_info_for_table(*, session: AsyncSession, user_id:int):
    query = select(BacketTable).where(BacketTable.c.user_id == user_id)
    result = await session.execute(query)
    return result.mappings().all()

async def get_info_back_for_id(*,session:AsyncSession, backet_id:int):
    query = select(BacketTable.c.user_id, BacketTable.c.order_id).where(BacketTable.c.id == backet_id)
    result = await session.execute(query)
    return result.mappings().all()

async def delete_item_backet(*,session:AsyncSession, backet_id:int):
    query = delete(BacketTable).where(BacketTable.c.id == backet_id)
    await session.execute(query)
    await session.commit()