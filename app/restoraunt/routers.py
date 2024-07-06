from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from typing import Annotated, List
from auth.models import User
from .schemas import (BaseRestorauntSchema, AddNewRestoraunt, ShowFullInfoRestoraunt,
    AddMenuSchema,AddNewCategorSchema,
    AddDishiesSchema, ContatSchema,
    )
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
        restaraunt_menu = await get_restaraunt_menu(restoraunt_id=restoraunt_id, session=session_param)
        #Если меню ресторана не вернулось
        if restaraunt_menu == (None,):
            await add_new_info_for_menu(restoraunt_id=restoraunt_id, **info_for_menu.model_dump(), session=session_param)
            return Response(content="Создание объекта меню произошло успешно!", status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вашего ресторана уже есть меню.')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')




#Добавление категории в меню
@router.post('/add_new_category/{restoraunt_id}/{menu_id}')
async def create_category_menu(restoraunt_id:int, menu_id:int,info_category: AddNewCategorSchema, current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Есди пользователь явялется основателем ресторана
    if verifeied_user:
        #Получение айди меню по прямой зависмости с рестораном
        await add_new_category_for_menu(**info_category.model_dump(),  session=session_param, menu_id=menu_id)
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


#Добавление контактной информации по ресторану
@router.post('/add_contact_info/{restoraunt_id}/')
async def add_contact_info(contact_info: ContatSchema,restoraunt_id:int,current_user: Annotated[User, Depends(get_current_user)],  session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    #Есди пользователь явялется основателем ресторана
    if verifeied_user:
        contact_info_for_restoraunt = await get_contact_info(session=session_param, restoraunt_id=restoraunt_id)
        if contact_info_for_restoraunt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть контактная информация')
        await add_new_contact_info_for_restorant(**contact_info.model_dump(), restoraunt_id=restoraunt_id, session=session_param)
        return Response(content="Создание контактной информации произошло успешно!", status_code=status.HTTP_201_CREATED)

    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')


    

async def get_list_products_for_menu(*, restoraunt_id, session):
    category_info_list:list = await get_category_orm(restoraunt_id=restoraunt_id, session=session)
    list_category_dishayes:list = []
    for one_category_info in category_info_list:
        dict_category: dict = {}
        products_list_dict_for_category = await get_list_products_for_category(category_id=one_category_info['id'], session=session)
        
        dict_category[one_category_info["title"]] = products_list_dict_for_category
        list_category_dishayes.append(dict_category)
    return list_category_dishayes




@router.get('/get_info_restoraunt/{restoraunt_id}', )#response_model=ShowFullInfoRestoraunt)
async def get_restoraunt_by_id(restoraunt_id: int, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    base_result_by_search:list = await get_info_restoraunt_by_id(restoraunt_id=restoraunt_id, session=session_param)
    if base_result_by_search:
        #Получение контактной информации
        contact_info = await get_contact_info(restoraunt_id=restoraunt_id, session=session_param)
        list_category_dishayes = await get_list_products_for_menu(restoraunt_id=restoraunt_id, session=session_param)
        base_info_restoraunt = {**base_result_by_search[0]}
        base_menu_info = await get_menu_info_for_orm(restoraunt_id=restoraunt_id, session=session_param)
        data_itog = {"base_restoraunt_info" : base_info_restoraunt, "contact_information" : {**contact_info[0]}, 'base_menu_info' : base_menu_info, "menu_list" : list_category_dishayes}
        return data_itog
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким id нет')

