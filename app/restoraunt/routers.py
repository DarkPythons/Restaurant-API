from fastapi import APIRouter, Depends, HTTPException, status, Path
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
    get_title_restoraunt,
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
from .utils import user_is_osvov_restoraunt, get_menu_id_func, get_info_title_rest, PathParamsDescription
from baselog import custom_log_app, generate_response_error

router = APIRouter()


@router.post('/create_new_restoraunt/', response_class=ORJSONResponse, summary='Create/upload new restoraunt')
async def create_new_restoraunt(
    current_user: Annotated[User, Depends(get_current_user)], 
    restoraunt_info: AddNewRestoraunt, 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавления ресторана"""
    restoraunt_title_in_db = await get_title_restoraunt(session=session_param, title=restoraunt_info.title)
    if not restoraunt_title_in_db:
        try:
            await create_restoraunt_orm(**restoraunt_info.model_dump(), user_id=current_user.id, session=session_param)
            custom_log_app.info(f"Ресторан с названием {restoraunt_info.title} был добавлен в базу.")
            return ORJSONResponse(
            content={'content' : f'Ресторан с названием {restoraunt_info.title} успешно добавлен в базу!'}, 
            status_code=status.HTTP_201_CREATED
            )
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ресторан с таким названием уже есть!')


@router.post('/add_menu_baseinfo/{restoraunt_id}', summary='Add base info in menu')
async def create_meny_baseinfo(
    restoraunt_id: Annotated[int, PathParamsDescription.restoraunt_id.value], 
    current_user: Annotated[User, Depends(get_current_user)], 
    info_for_menu: AddMenuSchema, 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Фукнция для добавления базовой информации для меню ресторана по его айди"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        restaraunt_menu = await get_restaraunt_menu(restoraunt_id=restoraunt_id, session=session_param)
        if restaraunt_menu == (None,):
            try:
                await add_new_info_for_menu(restoraunt_id=restoraunt_id, **info_for_menu.model_dump(), session=session_param)
                custom_log_app.info(f"Меню для ресторана с id {restoraunt_id} было добавлено")
                return ORJSONResponse(content={"content" : "Создание объекта меню произошло успешно!"}, status_code=status.HTTP_201_CREATED)
            except Exception as Error:
                await generate_response_error(Error)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вашего ресторана уже есть меню.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='У вас нет доступа на изменение информации этого ресторана'
        )




@router.post('/add_new_category/{restoraunt_id}/{menu_id}', summary='Add new category')
async def create_category_menu(
    restoraunt_id:Annotated[int, PathParamsDescription.restoraunt_id.value], 
    menu_id:Annotated[int, PathParamsDescription.menu_id.value],
    info_category: AddNewCategorSchema,
    current_user: Annotated[User, Depends(get_current_user)],  
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавление новой категории по айди ресторана и меню"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_func(restoraunt_id=restoraunt_id, session_param=session_param)
        if menu_id_for_orm == menu_id:
            try:
                await add_new_category_for_menu(
                **info_category.model_dump(),  
                session=session_param, 
                menu_id=menu_id_for_orm, 
                restoraunt_id=restoraunt_id
                )
                custom_log_app.info(f"Произошло добавление новой категории в меню с id {menu_id}")
                return ORJSONResponse(content={"content" : "Создаение категории произошло успешно!"}, status_code=status.HTTP_201_CREATED)
            except Exception as Error:
                await generate_response_error(Error)
        else:
            raise HTTPException(status_code=404, detail='У данного ресторана не такой menu_id.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')


@router.post('/add_new_dishaes/{restoraunt_id}/{menu_id}/{category_id}/', summary='Add new dishaes')
async def add_new_dishaes_with_category(
    restoraunt_id:Annotated[int, PathParamsDescription.restoraunt_id.value],
    menu_id:Annotated[int, PathParamsDescription.menu_id.value], 
    category_id:Annotated[int, PathParamsDescription.category_id.value], 
    list_of_dishies: List[AddDishiesSchema],
    current_user: Annotated[User, Depends(get_current_user)],  
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добалвение нового блюда в меню, по айди ресторана, меню, категории, со всеми проверками"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        menu_id_for_orm = await get_menu_id_func(restoraunt_id=restoraunt_id, session_param=session_param)
        if menu_id_for_orm == menu_id:
            category_on_menu = await get_category_for_menu(menu_id=menu_id, session=session_param)
            if category_id in category_on_menu:
                try:
                    await add_new_dishaes_on_category(list_of_dishies=list_of_dishies, 
                    session=session_param, 
                    category_id=category_id,
                    restoraunt_id=restoraunt_id,
                    menu_id=menu_id)
                    custom_log_app.info(f"Добавление нового блюда в меню с id {menu_id} прошло успешно.")
                    return ORJSONResponse(content={"content" : "Занесение блюда в меню произошло успешно!"}, status_code=status.HTTP_201_CREATED)
                except Exception as Error:
                    await generate_response_error(Error)
            else:
                raise HTTPException(status_code=404, detail='Категории с таким id в данном меню не найдено.')
        else:
            raise HTTPException(status_code=404, detail='Меню с таким айди у этого ресторана нет.')
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на \
        изменение информации этого ресторана')
    
@router.post('/add_contact_info/{restoraunt_id}/', summary="Add contact info")
async def add_contact_info(contact_info: AddContantSchema,
    restoraunt_id:Annotated[int, PathParamsDescription.restoraunt_id.value],
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавление контактной информации ресторану"""
    verifeied_user = await user_is_osvov_restoraunt(restoraunt_id=restoraunt_id, current_user=current_user, session=session_param)
    if verifeied_user == 200:
        contact_info_for_restoraunt = await get_contact_info(session=session_param, restoraunt_id=restoraunt_id)
        if contact_info_for_restoraunt:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='У вас уже есть контактная информация')
        try:
            await add_new_contact_info_for_restorant(**contact_info.model_dump(), restoraunt_id=restoraunt_id, session=session_param)
            custom_log_app.info(f"Добавление контактной информации для ресторана с id {restoraunt_id} прошло успешно.")
            return ORJSONResponse(content={"content" : "Добавление контактной информации успешно произошло!"}, \
                status_code=status.HTTP_201_CREATED)
        except Exception as Error:
            await generate_response_error(Error)     
    elif verifeied_user == 'Not restoraunt':
        raise HTTPException(status_code=404, detail='Ресторана с таким id не найдено.')
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет доступа на изменение информации этого ресторана')


@router.get('/get_info_restoraunt/{restoraunt_id}', response_model=ShowFullInfoRestoraunt, summary='View info restorunt by id')
async def get_restoraunt_by_id(
    restoraunt_id: Annotated[int, PathParamsDescription.restoraunt_id.value], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Фунция для получения полной информации по id ресторана"""
    base_result_by_search:list = await get_info_restoraunt_by_id(restoraunt_id=restoraunt_id, session=session_param)
    if base_result_by_search:
        try:
            data_itog = await get_data_itog_for_restoraunt(
                restoraunt_id=restoraunt_id, session=session_param, 
                base_result_by_search=base_result_by_search
                )
            custom_log_app.info(f"Получение информации по ресторану с id {restoraunt_id} произошло успешно.")
            return data_itog
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким id нет')


@router.get('/get_info_for_restoaunt/{title}', response_model=ShowFullInfoRestoraunt, summary="View info restoraunt")
async def get_info_for_restoaunt(
    title:Annotated[str, Path(title='Название ресторана', description='Введите название ресторана:')], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получение полной информации по названию ресторана"""
    id_for_restoraunt_by_id = await get_info_for_restoraunt_orm(title_rest=title, session=session_param)
    if id_for_restoraunt_by_id:
        try:
            data_itog = await get_info_title_rest(rest_id=id_for_restoraunt_by_id, session=session_param)
            custom_log_app.info(f"Получение информации по ресторану с названем {title} произошло успешно.")
            return data_itog
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ресторана с таким названием нет')
    