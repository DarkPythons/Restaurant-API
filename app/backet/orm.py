from .models import BacketTable
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def add_new_item_for_backet_orm(*,session: AsyncSession, item_id:int, user_id:int, in_order: bool):
    query = insert(BacketTable).values(user_id=user_id,item_id=item_id,in_order=in_order)
    await session.execute(query)
    await session.commit()