from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import get_current_user, create_message, get_info_func
from auth.models import User
from .schemas import AddNewCourierShemas, SelectStatus
from .orm import *
from database import get_async_session

router_courier = APIRouter()

@router_courier.post('/add_new_courier/{user_id}')
async def add_new_courier(
    user_id:int, 
    current_user: Annotated[User, Depends(get_current_user)], 
    info_for_courier_add: AddNewCourierShemas, 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для добавления нового курьера в базу (по айди человека, который уже есть в базе приложения)"""
    #Только человек с правами админа может выдавать права курьера человеку
    if current_user.is_superuser:
        user_id_is_not_null = await get_user_in_table_user(session=session_param, user_id=user_id)
        if user_id_is_not_null:
            courier_id_in_courier_table = await get_user_in_coruier_table(session=session_param, user_id=user_id)
            if not courier_id_in_courier_table:
                await add_new_courier_orm(session=session_param, user_id=user_id, info_for_courier_add=info_for_courier_add)
                user_info:dict= user_id_is_not_null[0]
                return ORJSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content={'content' : f'Пользователь {user_info['first_name']} {user_info['last_name']}, с айди {user_id} был добавлен в таблицу курьеров'}
                )
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Человек с этим id уже явялется курьером')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Человека с таким id нет в таблице юзеров.')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет прав на добавление курьеров.')

@router_courier.post('/update_my_status_work/')
async def update_my_status_work(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    in_work: bool
):
    """Функция для обновления статуса курьера (работает или нет)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        await update_info_for_table_courier(session=session_param, user_id=current_user.id, in_work=in_work)
        message = await create_message(in_work)
        return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : f'Ваш статус работы обновлен на: {message}'})
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете обновлять статус работы.'
        )
    
@router_courier.post("/verified_my_courier_account/")
async def get_my_verified_courier(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для подтверждения аккаунта курьера (без логики проверки)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        courier_info = courier_info[0]
        if not courier_info['verified']:
            await update_status_verified_user(session=session_param, user_id=current_user.id)
            return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : f'Ваш статус верификации обновлен'})
        else:
            raise HTTPException(status_coded=status.HTTP_400_BAD_REQUEST, detail='Вы уже верифицированный курьер')
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не являетесь курьером, поэтому не можете получить верификацию для курьеров.'
        )

@router_courier.post('/take_order/{order_id}')
async def take_order(
    order_id:int,
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для взятия заказов курьером"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        courier_info = courier_info[0]
        if courier_info['verified']:
            order_info = await get_order_info_for_id(order_id=order_id, session=session_param)
            if order_info:
                if not courier_info['in_work']:
                    await update_info_for_table_courier(session=session_param, user_id=current_user.id, in_work=True)
                await update_curier_orders(session=session_param, order_id=order_id, courier_id=courier_info['id'])
                return ORJSONResponse(
                status_code=status.HTTP_202_ACCEPTED, 
                content={'content' : f'Вы добавили заказ номер {order_id} к своим заказам, хорошей доставки.'}
                )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id нет, или этот заказ уже чей-то') 
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не верифицировали свой аккаунт!') 
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не являетесь курьером, поэтому не можете взять заказ.')  

@router_courier.get('/get_my_active_order/')
async def viev_order_user(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info: 
        courier_info = courier_info[0]
        courier_id = courier_info['id']
        all_active_order:list = await get_active_order_courier(session=session_param, courier_id=courier_id)
        return all_active_order
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не являетесь курьером, поэтому не можете взять заказ.')  

@router_courier.get('/get_info_account')
async def get_my_info_account(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получения информации о профиле курьера (активные заказы, телефон, mail и тд.)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        data_info = await get_info_func(courier_info)
        return {'account_info' : data_info}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете получить информацию об аккаунте курьерa.'
        )    

@router_courier.get('/get_orders_all/')
async def get_order_all(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получения информации об заказах, которые сделали люди"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        result = await get_order_all_no_courier(session=session_param)
        return result
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете получать информацию об свободных заказах.'
        )    


@router_courier.put('/update_status_order/{order_id}')
async def update_status_order(
    order_id:int, 
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    new_status: SelectStatus = Depends()
):
    """Функция для обновления статуса заказа, который доставляет курьер"""
    new_stat = new_status.model_dump()['new_status'].value
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info: 
        courier_info = courier_info[0]
        order_info = await get_order_info_for_id(order_id=order_id, session=session_param, courier_id=courier_info['id'])
        if order_info:
            order_info = order_info[0]
            if order_info['status'] != 'Доставлен':
                await update_status_this_order(order_id=order_id, session=session_param, status=new_stat)
                return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : 'Вы успешно обновили статус заказа'})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Вы не можете изменять статус доставленных заказов')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id нет, или у вас нет заказа с таким id')
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не являетесь курьером, поэтому не можете обновлять статус заказа'
        ) 