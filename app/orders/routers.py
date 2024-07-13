from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from .utils import get_current_user, get_spisok_order_full_func
from auth.models import User
from .orm import (
    get_backet_item_for_user_id, 
    get_active_order_fo_user, 
    get_order_by_id,
    get_order_user_by_orderId,
    delete_order_by_id,
    )
from .utils import create_new_order_func, PathOrderDescription
from database import get_async_session
from .schemas import StatusForOrder
from baselog import custom_log_app, generate_response_error

router_order = APIRouter()


@router_order.get('/view_my_active_order/', summary='View my active order')
async def get_my_active_order_list(
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Функция для получения активных заказов пользователя"""
    try:
        active_order_user = await get_active_order_fo_user(session=session_param, user_id=current_user.id)
        custom_log_app.info(f"Пользователь с id {current_user.id} получил свои активные заказы.")
        return {'active_order' : active_order_user}
    except Exception as Error:
        await generate_response_error(Error)

@router_order.get('/view_full_info_order/{order_id}')
async def view_full_info(
    order_id: Annotated[int, PathOrderDescription.order_id.value], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Функция для получения полной информации по id заказа"""
    order_info = await get_order_user_by_orderId(session=session_param, order_id=order_id, user_id=current_user.id)
    if order_info:
        try:
            order_info = order_info[0]
            data_full_spisok = await get_spisok_order_full_func(order_info=order_info, session=session_param, order_id=order_id)
            data_itog = {"order_info" : order_info, 'full_data_for_items' : data_full_spisok}
            custom_log_app.info(f"Пользователь с id {current_user.id} запросил полную информацию об заказе с id {order_id}")
            return data_itog
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вашего активного заказа с таким id не найдено")

@router_order.post('/add_new_order/', summary='Add new order in db')
async def add_new_order(
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)], 
    address: str
):
    """Функция для создания заказа, при которой все товары из корзины становятся товаром из заказа"""
    item_backet_for_user_no_active_order = await get_backet_item_for_user_id(session=session_param, user_id=current_user.id)
    if item_backet_for_user_no_active_order:
        try:
            await create_new_order_func(item_backet_for_user_no_active_order, session_param, current_user, address)
            custom_log_app.info(f"Пользователь с id {current_user.id} сделал заказ с адресом {address}.")
            return ORJSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content={'content' : 'Добавление нового заказа произошло успешно!'}
            )
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail='Вы не можете оформить заказ с пустой корзиной, или корзиной где только товары активных заказов.'
        )
    



@router_order.delete('/delete_my_order/{order_id}', summary='Delete order by order_id')
async def delete_user_order_id(
    order_id: Annotated[int, PathOrderDescription.order_id.value], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Функция для удаления заказа у человека, по его id"""
    active_order_user:list = await get_order_by_id(session=session_param, order_id=order_id)
    if active_order_user:
        active_order_user:dict = active_order_user[0]
        if active_order_user['user_id'] == current_user.id:
            #Если статус заказа только в готовке
            if active_order_user['status'] == StatusForOrder.cooking.value:
                try:
                    await delete_order_by_id(order_id=order_id, session=session_param)
                    custom_log_app.info(f"Пользователь с id {current_user.id} отменил заказ с id {order_id}")
                    return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : 'Отмена заказа успешно произошла'})
                except Exception as Error:
                    await generate_response_error(Error)
            else:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Вы не можете отменить заказ, который имеет статус выше "готовки".'
                )
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='у вас нет прав на отмену чужик заказов')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id не найдено')

