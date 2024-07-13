from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from .utils import get_current_user
from auth.models import User
from .orm import (
    get_list_id_items,
    add_new_item_for_backet_orm,
    get_raw_info_for_table,
    get_info_back_for_id,
    delete_item_backet,
)
from database import get_async_session
from .utils import get_data_list_func
from baselog import custom_log_app, generate_response_error

router_backet = APIRouter()

@router_backet.get('/get_my_backet/', summary='Get my full backet')
async def get_backet_for_user(
    current_user: Annotated[User, Depends(get_current_user)],
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для поучения корзины человека"""
    items_for_backet = await get_raw_info_for_table(session=session_param, user_id=current_user.id)
    if items_for_backet:
        try:
            itog_list_data: list = await get_data_list_func(items_for_backet, session_param)
            custom_log_app.info(f"Пользователь с id {current_user.id} запросил свою корзину.")
            return itog_list_data
        except Exception as Error:
            await generate_response_error(Error)
    else:
        return ORJSONResponse(status_code=200, content={'content' : []}) 
    
    
@router_backet.post('/add_new_item_for_backet/{item_id}', summary='Add new item in backet')
async def add_new_item_for_backet(
    current_user: Annotated[User, Depends(get_current_user)],
    item_id:Annotated[int, Path(title='Айди предмета', description='Введите айди предмета:', ge=1)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция добавления элемента из меню любого ресторана по его id"""
    list_id_for_items_menu:list = await get_list_id_items(session=session_param)
    if item_id in  list_id_for_items_menu:
        try:
            await add_new_item_for_backet_orm(user_id=current_user.id, item_id=item_id, session=session_param, order_id=None)
            custom_log_app.info(f"Добавление элемента с id {item_id} \
                в корзину пользователя с id {current_user.id} прошло успешно")
            return ORJSONResponse(status_code=201, content={'content' : 'Вы успешно добавили новый предмет в корзину'}) 
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Предмета с таким айди не найдено')


@router_backet.delete('/delete_item/{backet_id}', summary='Delete item in my backet by id')
async def delete_one_item_bakcet(
    backet_id:Annotated[int, Path(title='Айди элемента корзины', description="Введите aйди элемента корзины:")], 
    current_user: Annotated[User, Depends(get_current_user)],
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для удаления элемента из своей корзины по его id в самой корзине"""
    backet_item_user:list = await get_info_back_for_id(backet_id=backet_id, session=session_param)
    if backet_item_user:
        backet_item_user:dict = backet_item_user[0]
        if backet_item_user['user_id'] == current_user.id:
            if not backet_item_user['order_id']:
                try:
                    await delete_item_backet(backet_id=backet_id, session=session_param)
                    custom_log_app.info(f"Пользователь с id {current_user.id} удалил объект из корзины с id {backet_id}")
                    return ORJSONResponse(
                        status_code=200, 
                        content={f'content' : f'Вы успешно удалили элемент корзины с айди: {backet_id}'}
                        )
                except Exception as Error:
                    await generate_response_error(Error)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail='Вы пытается удалить элемент корзины, который есть в действующем заказе.'
                    )
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы пытаетесь удалить элемент чужой корзины.')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Вы пытаетесь удалить элемент, айди которого нет.')