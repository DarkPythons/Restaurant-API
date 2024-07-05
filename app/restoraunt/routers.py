from fastapi import APIRouter, Depends, HTTPException, status
from .utils import get_current_user
from typing import Annotated, List
from auth.models import User
from .schemas import BaseRestorauntSchema, AddNewRestoraunt, ShowInfoRestoraunt,AddMenuSchema,AddNewCategorSchema,AddDishiesSchema
from .orm import *
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter()

#Развертывание своего ресторана
@router.post('/create_new_restoraunt/')
async def create_new_restoraunt(current_user: Annotated[User, Depends(get_current_user)], restoraunt_info: AddNewRestoraunt, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    #Проверка, есть ли ресторан с таким же названием

    await create_restoraunt_orm(**restoraunt_info.model_dump(), user_id=current_user.id, session=session_param)





async def user_is_osvov_restoraunt(*, restoraunt_id, current_user,session):
    restoraunt_user_osnovatel = await get_restoraunt_osnov_for_id_rest(session=session, restoraunt_id=restoraunt_id)
    if current_user.id == restoraunt_user_osnovatel[0]:
        return True
    else:
        return False



#Создаение объекта меню к своему ресторану
@router.post('/add_menu_baseinfo/{restoraunt_id}')
async def create_meny_baseinfo(restoraunt_id:int, current_user: Annotated[User, Depends(get_current_user)], info_for_menu: AddMenuSchema, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Если юзер является основателем ресторана
    if verifeied_user:
        await add_new_info_for_menu(restoraunt_id=restoraunt_id, **info_for_menu.model_dump(), session=session_param)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')




#Добавление категории в меню
@router.post('/add_new_category/{restoraunt_id}/')
async def create_category_menu(restoraunt_id:int, info_category: AddNewCategorSchema, current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Есди пользователь явялется основателем ресторана
    if verifeied_user:
        #Получение айди меню по прямой зависмости с рестораном
        menu_id = await get_info_for_menu_restoraunt(session=session_param, restoraunt_id=restoraunt_id)
        await add_new_category_for_menu(**info_category.model_dump(),  session=session_param, menu_id=menu_id[0])
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')

#Добавление новоых блюд в меню
@router.post('/add_new_dishaes/{restoraunt_id}/{menu_id}/{category_id}/')
async def add_new_dishaes_with_category(menu_id:int, list_of_dishies: List[AddDishiesSchema],restoraunt_id:int, category_id:int, current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Есди пользователь явялется основателем ресторана
    if verifeied_user:
        category_on_menu = await get_category_for_menu(menu_id=menu_id,restoraunt_id=restoraunt_id,category_id=category_id, session=session_param)
        if category_on_menu:
            await add_new_dishaes_on_category(list_of_dishies=list_of_dishies, session=session_param, category_id=category_id)
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')




#Просмотр всей информации по ресторану по названию / адресу / айди
@router.get('/get_info_restoraunt/{restoraunt_id}')
async def get_restoraunt_by_id(restoraunt_id: int, session_param: Annotated[AsyncSession, Depends(get_async_session)]) :#->  ShowInfoRestoraunt:
    base_result_by_search = await get_info_restoraunt_by_id(restoraunt_id=restoraunt_id, session=session_param)
    if base_result_by_search:
        return base_result_by_search
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким id нет')

