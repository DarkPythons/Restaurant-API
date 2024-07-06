from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from typing import Annotated, List
from auth.models import User
from .schemas import (BaseRestorauntSchema, AddNewRestoraunt, ShowFullInfoRestoraunt,
    AddMenuSchema,AddNewCategorSchema,
    AddDishiesSchema, ContatSchema, ListGetDishiesSchema, BaseDishesSchema
    )
from .orm import *
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse
from .utils import user_is_osvov_restoraunt, get_list_products_for_menu
from sqlalchemy.exc import NoResultFound
router = APIRouter()

#Создаение ресторана
@router.post('/create_new_restoraunt/', response_class=ORJSONResponse)
async def create_new_restoraunt(current_user: Annotated[User, Depends(get_current_user)], restoraunt_info: AddNewRestoraunt, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    #Проверка, есть ли ресторан с таким же названием
    list_restoraunt_title = await get_list_title_restoraunt(session=session_param)
    if not restoraunt_info.title in list_restoraunt_title:
        await create_restoraunt_orm(**restoraunt_info.model_dump(), user_id=current_user.id, session=session_param)
        return ORJSONResponse(content={'content' : f'Ресторан с названием {restoraunt_info.title} успешно добавлен в базу!'}, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ресторан с таким названием уже есть!')

#Добавление базовой информации в меню ресторана
@router.post('/add_menu_baseinfo/{restoraunt_id}')
async def create_meny_baseinfo(restoraunt_id:int, current_user: Annotated[User, Depends(get_current_user)], info_for_menu: AddMenuSchema, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        restaraunt_menu = await get_restaraunt_menu(restoraunt_id=restoraunt_id, session=session_param)
        if restaraunt_menu == (None,):
            await add_new_info_for_menu(restoraunt_id=restoraunt_id, **info_for_menu.model_dump(), session=session_param)
            return ORJSONResponse(content={"content" : "Создание объекта меню произошло успешно!"}, status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вашего ресторана уже есть меню.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')
    
#Добавление категории в меню
@router.post('/add_new_category/{restoraunt_id}/{menu_id}')
async def create_category_menu(restoraunt_id:int, menu_id:int,info_category: AddNewCategorSchema, current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_for_restoraunt(restoraunt_id=restoraunt_id, session=session_param)
        menu_id_for_orm = int(menu_id_for_orm[0][0])
        if menu_id_for_orm == menu_id:
            await add_new_category_for_menu(**info_category.model_dump(),  session=session_param, menu_id=menu_id_for_orm, restoraunt_id=restoraunt_id)
            return ORJSONResponse(content={"content" : "Создаение категории произошло успешно!"}, status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=404, detail='У данного ресторана не такой menu_id.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')

#Добавление новоых блюд в меню
@router.post('/add_new_dishaes/{restoraunt_id}/{menu_id}/{category_id}/')
async def add_new_dishaes_with_category(menu_id:int, list_of_dishies: List[AddDishiesSchema],restoraunt_id:int, category_id:int, current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_for_restoraunt(restoraunt_id=restoraunt_id, session=session_param)
        menu_id_for_orm = int(menu_id_for_orm[0][0])
        if menu_id_for_orm == menu_id:
            category_on_menu = await get_category_for_menu(menu_id=menu_id, session=session_param)
            if category_id in category_on_menu:
                await add_new_dishaes_on_category(list_of_dishies=list_of_dishies, session=session_param, category_id=category_id,restoraunt_id=restoraunt_id,menu_id=menu_id)
                return ORJSONResponse(content={"content" : "Занесение блюда в меню произошло успешно!"}, status_code=status.HTTP_201_CREATED)
            else:
                raise HTTPException(status_code=404, detail='Категории с таким id в данном меню не найдено.')
        else:
            raise HTTPException(status_code=404, detail='Меню с таким айди у этого ресторана нет.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')
    
#Добавление контактной информации по ресторану
@router.post('/add_contact_info/{restoraunt_id}/')
async def add_contact_info(contact_info: ContatSchema,restoraunt_id:int,current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Есди пользователь явялется основателем ресторана
    if verifeied_user == 200:
        contact_info_for_restoraunt = await get_contact_info(session=session_param, restoraunt_id=restoraunt_id)
        if contact_info_for_restoraunt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть контактная информация')
        await add_new_contact_info_for_restorant(**contact_info.model_dump(), restoraunt_id=restoraunt_id, session=session_param)
        return Response(content="Создание контактной информации произошло успешно!", status_code=status.HTTP_201_CREATED)
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')










@router.get('/get_info_restoraunt/{restoraunt_id}', response_model=ShowFullInfoRestoraunt)
async def get_restoraunt_by_id(restoraunt_id: int, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    base_result_by_search:list = await get_info_restoraunt_by_id(restoraunt_id=restoraunt_id, session=session_param)
    if base_result_by_search:
        #Получение контактной информации
        contact_info_itog = {}
        contact_info = await get_contact_info(restoraunt_id=restoraunt_id, session=session_param)
        if contact_info:
            contact_info_itog = {**contact_info[0]}
        list_category_dishayes = await get_list_products_for_menu(restoraunt_id=restoraunt_id, session=session_param)
        base_info_restoraunt = {**base_result_by_search[0]}
        base_menu_info = await get_menu_info_for_orm(restoraunt_id=restoraunt_id, session=session_param)
        if not base_menu_info:
            base_menu_info = {}
        else:
            base_menu_info = base_menu_info[0]
        data_itog = {"base_restoraunt_info" : base_info_restoraunt, "contact_information" : contact_info_itog, 'base_menu_info' : base_menu_info, "menu_list" : list_category_dishayes}
        return data_itog
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким id нет')

