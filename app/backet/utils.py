from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User
from .orm import get_info_for_orm

fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()


async def get_data_list_func(items_for_backet, session_param):
    """Функция для перебота элементов в корзине и возврат их с новыми данными"""
    itog_list_data: list = []
    for one_item_for_bakcet in items_for_backet:
        #Данные каждого элемента в корзине
        data:list = {}
        data['metainfo'] = {
        "backet_id" : one_item_for_bakcet['id'], 
        'user_id' : one_item_for_bakcet['user_id'], 
        "item_id" :  one_item_for_bakcet['item_id'], 
        'order_id' : one_item_for_bakcet['order_id']
        }
        #Добавление информации об самом item
        item_info_orm = await get_info_for_orm(session=session_param, item_id=one_item_for_bakcet['item_id'])
        item_info_orm = item_info_orm[0]
        data['item_info'] = []
        data['item_info'].append(item_info_orm)
        itog_list_data.append(data)
    return itog_list_data