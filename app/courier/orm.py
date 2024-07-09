from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .models import CourierTable
from .schemas import AddNewCourierShemas
from auth.models import user
from orders.models import OrderTable

async def add_new_courier_orm(session:AsyncSession, user_id, info_for_courier_add: AddNewCourierShemas):
    query = insert(CourierTable).values(user_id=user_id, **info_for_courier_add.model_dump())
    await session.execute(query)
    await session.commit()


async def get_user_in_coruier_table(*, session, user_id):
    query = select(CourierTable).where(CourierTable.c.user_id == user_id)
    result = await session.execute(query)
    return result.mappings().all()


async def get_user_in_table_user(*, session, user_id):
    query = select(user.c.id, user.c.first_name, user.c.last_name).where(user.c.id == user_id)
    result = await session.execute(query)
    return result.mappings().all()
async def update_info_for_table_courier(*,session,user_id,in_work):
    query = update(CourierTable).values(in_work=in_work).where(CourierTable.c.user_id == user_id)
    await session.execute(query)
    await session.commit()


async def update_status_verified_user(*, session, user_id):
    query = update(CourierTable).values(verified=True).where(CourierTable.c.user_id == user_id)
    await session.execute(query)
    await session.commit()

async def get_order_all_no_courier(*, session):
    query = select(OrderTable).where(OrderTable.c.courier_id == None)
    result = await session.execute(query)
    return result.mappings().all()

async def get_order_info_for_id(*, session, order_id, courier_id=None):
    query = select(OrderTable).where(and_(OrderTable.c.id == order_id), OrderTable.c.courier_id == courier_id)
    result = await session.execute(query)
    return result.mappings().all()

async def update_curier_orders(*, session,order_id,courier_id):
    query = update(OrderTable).values(courier_id=courier_id).where(OrderTable.c.id == order_id)
    await session.execute(query)
    await session.commit()

async def get_active_order_courier(*, session, courier_id):
    query = select(OrderTable).where(and_(OrderTable.c.courier_id == courier_id), OrderTable.c.status != 'Доставлен')
    result = await session.execute(query)
    return result.mappings().all()


async def update_status_this_order(*, session, order_id, status):
    query = update(OrderTable).values(status=status).where(OrderTable.c.id == order_id)
    await session.execute(query)
    await session.commit()