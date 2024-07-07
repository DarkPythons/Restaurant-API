from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from auth.models import User
from typing import Annotated
from .orm import add_new_item_for_backet_orm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

router_backet = APIRouter()

@router_backet.post('/add_new_item_for_backet/{item_id}')
async def add_new_item_for_backet(current_user: Annotated[User, Depends(get_current_user)], item_id:int, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    await add_new_item_for_backet_orm(user_id=current_user.id, item_id=item_id, session=session_param, in_order=False)