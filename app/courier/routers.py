from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from auth.models import User
from typing import Annotated
from .schemas import AddNewCourierShemas
from .orm import add_new_courier_orm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
router_courier = APIRouter()

@router_courier.post('/add_new_courier/{user_id}')
async def add_new_courier(user_id:int, current_user: Annotated[User, Depends(get_current_user)], info_for_courier_add: AddNewCourierShemas, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    #Только человек с правами админа может добавлять новых курьеров
    if current_user.is_superuser:
        await add_new_courier_orm(session=session_param, user_id=user_id, info_for_courier_add=info_for_courier_add)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет прав на добавление курьеров.')