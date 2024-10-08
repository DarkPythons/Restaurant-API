from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User

fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()


def get_slovar_dates(*,courier_info, order_info):
    slovar_data = [{
        "email_courier" : courier_info['email'],
        "first_name_courier" : courier_info['first_name'],
        "last_name_courier" : courier_info['last_name'],
        "price_order":order_info['price_order'],
        "address_order":order_info['address'],
        "order_id":order_info['order_id'],
        "user_id":order_info['user_id'],
    }]
    return slovar_data

async def create_message(in_work):
    """Функия формирования ответа для соответствуюего запроса курьера"""
    message = 'Не в работе'
    if in_work:
        message = 'В работе'
    return message

async def get_info_func(couriers_info):
    """Фукнция преобразования полученных данных о курьере"""
    courier_info = couriers_info[0]
    data_info = {
    "first_name" : courier_info['first_name'],
    "last_name" : courier_info['last_name'],
    "phone" : courier_info['phone'],
    "in_work" : courier_info['in_work'],
    "verified" : courier_info['verified'],
    "email" : courier_info['email'],
    }
    return data_info