from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backet.models import BacketTable
from .schemas import StatusForOrder
from .models import OrderTable

async def get_backet_item_for_user_id(*,user_id:int, session:AsyncSession):
    query = select(BacketTable).where(and_(BacketTable.c.user_id == user_id), BacketTable.c.order_id == None)
    result = await session.execute(query)
    return result.mappings().all()

async def add_new_order_for_db(*, price_order,status=StatusForOrder.cooking.value,user_id,address,session):
    query = insert(OrderTable).values(price_order=price_order,status=status,address=address,user_id=user_id).returning(OrderTable.c.id)
    result = await session.execute(query)
    await session.commit()
    return result.first()

async def update_data_bakcet(*, user_id, session:AsyncSession, order_id:int):
    query = update(BacketTable).values(order_id=order_id).where(and_(BacketTable.c.user_id == user_id), BacketTable.c.order_id == None)
    await session.execute(query)
    await session.commit()

async def get_active_order_fo_user(*, user_id:int, session:AsyncSession):
    query = select(OrderTable).where(and_(OrderTable.c.user_id == user_id), OrderTable.c.status != StatusForOrder.delivered_finish.value)
    result = await session.execute(query)
    return result.mappings().all()

async def get_order_by_id(*, order_id:int, session:AsyncSession):
    query = select(OrderTable).where(OrderTable.c.id == order_id)
    result = await session.execute(query)
    return result.mappings().all()


async def delete_order_by_id(*, order_id:int, session:AsyncSession):
    query = delete(OrderTable).where(OrderTable.c.id == order_id)
    await session.execute(query)
    await session.commit()