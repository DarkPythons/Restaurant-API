from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import RassilkaBaseConfig
from .utils import get_current_user, create_message, get_info_func, get_slovar_dates
from auth.models import User
from .schemas import AddNewCourierShemas, SelectStatus
from .orm import *
from database import get_async_session
from orders.utils import PathOrderDescription
from .celery_config import send_email_message_courier
from baselog import custom_log_app, generate_response_error, custom_log_exception

rassilka_config = RassilkaBaseConfig()

router_courier = APIRouter()

@router_courier.post('/add_new_courier/{user_id}', summary='Add new courier')
async def add_new_courier(
    user_id:Annotated[int, Path(title='Айди пользователя', description='Введите айди пользователя из базы данных:', ge=1)], 
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
                try:
                    await add_new_courier_orm(session=session_param, user_id=user_id, info_for_courier_add=info_for_courier_add)
                    user_info:dict= user_id_is_not_null[0]
                    custom_log_app.info(f"Был создан курьер, привязанный к id пользователя: \
                        {user_id}, айди создател: {current_user.id}")
                    return ORJSONResponse(
                    status_code=status.HTTP_201_CREATED, 
                    content={'content' : f'Пользователь {user_info['first_name']} {user_info['last_name']}, \
                    с айди {user_id} был добавлен в таблицу курьеров'}
                    )
                except Exception as Error:
                    await generate_response_error(Error)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Человек с этим id уже явялется курьером')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Человека с таким id нет в таблице юзеров.')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет прав на добавление курьеров.')

@router_courier.post('/update_my_status_work/', summary='Update my status work')
async def update_my_status_work(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)], 
    in_work: bool
):
    """Функция для обновления статуса курьера (работает или нет)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        try:
            await update_info_for_table_courier(session=session_param, user_id=current_user.id, in_work=in_work)
            message = await create_message(in_work)
            custom_log_app.info(f"Курьер с id {courier_info[0]['id']}, обновил статус работы на {message}.")
            return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : f'Ваш статус работы обновлен на: {message}'})
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете обновлять статус работы.'
        )
    
@router_courier.post("/verified_my_courier_account/", summary='Verify my courier account')
async def get_my_verified_courier(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для подтверждения аккаунта курьера (без логики проверки)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        courier_info = courier_info[0]
        if not courier_info['verified']:
            try:
                await update_status_verified_user(session=session_param, user_id=current_user.id)
                custom_log_app.info(f"Курьер c id {courier_info['id']} подал заявку на верификацию аккаунта.")
                return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : f'Ваш статус верификации обновлен'})
            except Exception as Error:
                await generate_response_error(Error)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Вы уже верифицированный курьер')
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не являетесь курьером, поэтому не можете получить верификацию для курьеров.'
        )

@router_courier.post('/take_order/{order_id}', summary='Take order by id')
async def take_order(
    order_id:Annotated[int, PathOrderDescription.order_id.value],
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
                try:
                    if not courier_info['in_work']:
                        await update_info_for_table_courier(session=session_param, user_id=current_user.id, in_work=True)
                    custom_log_app.info(f"Курьер с id {courier_info['id']} взял заказ с id {order_id}")
                    await update_curier_orders(session=session_param, order_id=order_id, courier_id=courier_info['id'])
                    return ORJSONResponse(
                    status_code=status.HTTP_202_ACCEPTED, 
                    content={'content' : f'Вы добавили заказ номер {order_id} к своим заказам, хорошей доставки.'}
                    )
                except Exception as Error:
                    await generate_response_error(Error)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id нет, или этот заказ уже чей-то') 
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не верифицировали свой аккаунт!') 
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не являетесь курьером, поэтому не можете взять заказ.')  

@router_courier.get('/get_my_active_order/', summary='Get my active orders')
async def viev_order_user(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получения информации об заказах, которые принадлежат курьеру."""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info: 
        try:
            courier_info = courier_info[0]
            courier_id = courier_info['id']
            all_active_order:list = await get_active_order_courier(session=session_param, courier_id=courier_id)
            custom_log_app.info(f"Курьер с id {courier_id} запросил все свои заказы.")
            return all_active_order
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не являетесь курьером, поэтому не можете взять заказ.')  

@router_courier.get('/get_info_account', summary='Get info my courier account')
async def get_my_info_account(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получения информации о профиле курьера (телефон, mail и тд.)"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        try:
            data_info = await get_info_func(courier_info)
            custom_log_app.info(f"Курьер с id {courier_info[0]['id']} запросил информацию о своём аккаунте")
            return {'account_info' : data_info}
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете получить информацию об аккаунте курьерa.'
        )    

@router_courier.get('/get_orders_all/', summary='Get all my orders')
async def get_order_all(
    current_user: Annotated[User, Depends(get_current_user)], 
    session_param: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Функция для получения информации об заказах, которые сделали люди"""
    courier_info = await get_user_in_coruier_table(session=session_param, user_id=current_user.id)
    if courier_info:
        try:
            result = await get_order_all_no_courier(session=session_param)
            custom_log_app.info(f"Курьер с id {courier_info[0]['id']} запросил информацию об открытых заказах")
            return result
        except Exception as Error:
            await generate_response_error(Error)
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Вы не являетесь курьером, поэтому не можете получать информацию об свободных заказах.'
        )    


@router_courier.put('/update_status_order/{order_id}', summary='Update status my orders')
async def update_status_order(
    order_id:Annotated[int, PathOrderDescription.order_id.value], 
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
                try:
                    await update_status_this_order(order_id=order_id, session=session_param, status=new_stat)
                    #Если рассылка включена
                    if rassilka_config.RASSILKA_IN_EMAIL:
                        if new_stat == 'Доставлен':
                            slovar_data = get_slovar_dates(courier_info=courier_info,order_info=order_info)
                            send_email_message_courier.apply_async(args=(slovar_data))
                            custom_log_app.info(f"Курьеру с id {courier_info['id']} на почту {courier_info['email']} было отправлено письмо")
                    custom_log_app.info(f"Обновление статуса заказа с id {order_id}, на статус {new_stat} прошло успешно")
                except Exception as Error:
                    await generate_response_error(Error)
                    
                return ORJSONResponse(status_code=status.HTTP_200_OK, content={'content' : 'Вы успешно обновили статус заказа.'})
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Вы не можете изменять статус доставленных заказов')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Заказа с таким id нет, или у вас лично нет заказа с таким id')
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не являетесь курьером, поэтому не можете обновлять статус заказа'
        ) 