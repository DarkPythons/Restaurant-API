from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .models import CourierTable
from .schemas import AddNewCourierShemas

async def add_new_courier_orm(session:AsyncSession, user_id, info_for_courier_add: AddNewCourierShemas):
    query = insert(CourierTable).values(user_id=user_id, **info_for_courier_add.model_dump())
    await session.execute(query)
    await session.commit()