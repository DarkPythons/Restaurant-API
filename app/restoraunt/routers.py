from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from .utils import get_current_user, get_data_itog_for_restoraunt, get_contact_info
from auth.models import User
from .schemas import (
    AddNewRestoraunt, ShowFullInfoRestoraunt,
    AddMenuSchema,AddNewCategorSchema,
    AddDishiesSchema, AddContantSchema
)
from .orm import (
    get_list_title_restoraunt,
    create_restoraunt_orm,
    get_restaraunt_menu,
    add_new_info_for_menu,
    add_new_category_for_menu,
    get_category_for_menu,
    add_new_dishaes_on_category,
    add_new_contact_info_for_restorant,
    get_info_restoraunt_by_id,
    get_info_for_restoraunt_orm,
)
from database import get_async_session
from .utils import user_is_osvov_restoraunt, get_menu_id_func, get_info_title_rest


router = APIRouter()


@router.post('/create_new_restoraunt/', response_class=ORJSONResponse)
async def create_new_restoraunt(
    current_user: Annotated[User, Depends(get_current_user)], 
    restoraunt_info: AddNewRestoraunt, 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавления ресторана"""
    list_restoraunt_title = await get_list_title_restoraunt(session=session_param)
    if not restoraunt_info.title in list_restoraunt_title:
        await create_restoraunt_orm(**restoraunt_info.model_dump(), user_id=current_user.id, session=session_param)
        return ORJSONResponse(
        content={'content' : f'Ресторан с названием {restoraunt_info.title} успешно добавлен в базу!'}, 
        status_code=status.HTTP_201_CREATED
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ресторан с таким названием уже есть!')


@router.post('/add_menu_baseinfo/{restoraunt_id}')
async def create_meny_baseinfo(restoraunt_id:int, 
    current_user: Annotated[User, Depends(get_current_user)], 
    info_for_menu: AddMenuSchema, 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Фукнция для добавления базовой информации для меню ресторана по его айди"""
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
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='У вас нет доступа на изменение информации этого ресторана'
        )




@router.post('/add_new_category/{restoraunt_id}/{menu_id}')
async def create_category_menu(restoraunt_id:int, 
    menu_id:int,info_category: AddNewCategorSchema,
    current_user: Annotated[User, Depends(get_current_user)],  
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавление новой категории по айди ресторана и меню"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_func(restoraunt_id=restoraunt_id, session_param=session_param)
        if menu_id_for_orm == menu_id:
            await add_new_category_for_menu(
            **info_category.model_dump(),  
            session=session_param, 
            menu_id=menu_id_for_orm, 
            restoraunt_id=restoraunt_id
            )
            return ORJSONResponse(content={"content" : "Создаение категории произошло успешно!"}, status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=404, detail='У данного ресторана не такой menu_id.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')


@router.post('/add_new_dishaes/{restoraunt_id}/{menu_id}/{category_id}/')
async def add_new_dishaes_with_category(menu_id:int, 
    list_of_dishies: List[AddDishiesSchema],
    restoraunt_id:int,
    category_id:int, current_user: Annotated[User, Depends(get_current_user)],  
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добалвение нового блюда в меню, по айди ресторана, меню, категории, со всеми проверками"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_func(restoraunt_id=restoraunt_id, session_param=session_param)
        if menu_id_for_orm == menu_id:
            category_on_menu = await get_category_for_menu(menu_id=menu_id, session=session_param)
            if category_id in category_on_menu:
                await add_new_dishaes_on_category(list_of_dishies=list_of_dishies, 
                session=session_param, 
                category_id=category_id,
                restoraunt_id=restoraunt_id,
                menu_id=menu_id)
                return ORJSONResponse(content={"content" : "Занесение блюда в меню произошло успешно!"}, status_code=status.HTTP_201_CREATED)
            else:
                raise HTTPException(status_code=404, detail='Категории с таким id в данном меню не найдено.')
        else:
            raise HTTPException(status_code=404, detail='Меню с таким айди у этого ресторана нет.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')
    
@router.post('/add_contact_info/{restoraunt_id}/')
async def add_contact_info(contact_info: AddContantSchema,
    restoraunt_id:int,
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавление контактной информации ресторану"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        contact_info_for_restoraunt = await get_contact_info(session=session_param, restoraunt_id=restoraunt_id)
        if contact_info_for_restoraunt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть контактная информация')
        await add_new_contact_info_for_restorant(**contact_info.model_dump(), restoraunt_id=restoraunt_id, session=session_param)
        return ORJSONResponse(content={"content" : "Добавление контактной информации успешно произошло!"}, status_code=status.HTTP_201_CREATED)
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')



@router.get('/get_info_restoraunt/{restoraunt_id}', response_model=ShowFullInfoRestoraunt)
async def get_restoraunt_by_id(restoraunt_id: int, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    """Фунция для получения полной информации по id ресторана"""
    base_result_by_search:list = await get_info_restoraunt_by_id(restoraunt_id=restoraunt_id, session=session_param)
    if base_result_by_search:
        data_itog = await get_data_itog_for_restoraunt(
            restoraunt_id=restoraunt_id, session=session_param, 
            base_result_by_search=base_result_by_search
            )
        return data_itog
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким id нет')


@router.get('/get_info_for_restoaunt/{title}', response_model=ShowFullInfoRestoraunt)
async def get_info_for_restoaunt(title:str, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    """Функция для получение полной информации по названию ресторана"""
    id_for_restoraunt_by_id = await get_info_for_restoraunt_orm(title_rest=title, session=session_param)
    if id_for_restoraunt_by_id:
        data_itog = await get_info_title_rest(rest_id=id_for_restoraunt_by_id, session=session_param)
        return data_itog
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким названием нет')
    