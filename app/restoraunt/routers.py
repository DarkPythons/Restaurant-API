from fastapi import APIRouter, Depends
from .utils import get_current_user
from typing import Annotated
from auth.models import User
from .schemas import BaseRestorauntSchema, AddNewRestoraunt
from .orm import create_restoraunt_orm
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter()

#Разезение своего ресторана
@router.post('/create_new_restoraunt/')
async def create_new_restoraunt(current_user: Annotated[User, Depends(get_current_user)], restoraunt_info: AddNewRestoraunt, sessio_param: Annotated[AsyncSession, Depends(get_async_session)]):
    #Проверка, есть ли ресторан с таким же названием

    await create_restoraunt_orm(**restoraunt_info.model_dump(), user_id=current_user.id, session=sessio_param)




#Обновление данных о ресторане (только если человек явялется его создателем)




#Просмотр всей информации по ресторану по названию / адресу / айди