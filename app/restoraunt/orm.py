from .models import Restoraunt
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
async def create_restoraunt_orm(*, title,rating,address,description, user_id, session):
    query = insert(Restoraunt).values(title=title,rating=rating,address=address,description=description,user_id=user_id)
    await session.execute(query)
    await session.commit()