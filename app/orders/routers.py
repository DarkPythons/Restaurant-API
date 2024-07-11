from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from .utils import get_current_user
from auth.models import User
from .orm import (
    get_backet_item_for_user_id, 
    get_active_order_fo_user, 
    get_order_by_id,
    delete_order_by_id)
from .utils import create_new_order_func, PathOrderDescription
from database import get_async_session
from .schemas import StatusForOrder

router_order = APIRouter()


@router_order.post('/add_new_order/', summary='Add new order in db')
async def add_new_order(
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)], 
    address: str
):
    """Функция для создания заказа, при которой все товары из корзины становятся товаром из заказа"""
    item_backet_for_user_no_active_order = await get_backet_item_for_user_id(session=session_param, user_id=current_user.id)
    if item_backet_for_user_no_active_order:
        await create_new_order_func(item_backet_for_user_no_active_order, session_param, current_user, address)
        return ORJSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content={'content' : 'Добавление нового заказа произошло успешно!'}
        )
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail='Вы не можете оформить заказ с пустой корзиной, или корзиной где только товары активных заказов.'
        )
    

@router_order.get('/view_my_active_order/', summary='View my active order')
async def get_my_active_order_list(
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Функция для получения активных заказов пользователя"""
    active_order_user = await get_active_order_fo_user(session=session_param, user_id=current_user.id)
    return {'active_order' : active_order_user}


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
                await delete_order_by_id(order_id=order_id, session=session_param)
                return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : 'Отмена заказа успешно произошла'})
            else:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Вы не можете отменить заказ, который имеет статус выше "готовки".'
                )
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='у вас нет прав на отмену чужик заказов')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id не найдено')