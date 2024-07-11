from fastapi_users import FastAPIUsers
from enum import Enum
from fastapi import Path

from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User
from .orm import add_new_order_for_db,update_data_bakcet
from backet.orm import get_info_for_orm


fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()






class PathOrderDescription(Enum):
    order_id=Path(title='Айди заказа', description="Введите айди заказа:", ge=1)


async def create_new_order_func(item_backet_for_user_no_active_order, session_param, current_user, address):
    summs_price_zakaz = 0
    for one_item_backet in item_backet_for_user_no_active_order:
        item_id:int = one_item_backet['item_id']
        info_from_orm:list =await get_info_for_orm(session=session_param, item_id=item_id)
        if info_from_orm:
            info_from_orm:dict = info_from_orm[0]
        summs_price_zakaz += info_from_orm['price']
    #Добавление заказа в базу
    order_id = await add_new_order_for_db(
    price_order=summs_price_zakaz, 
    address=address, 
    user_id=current_user.id, 
    session=session_param
    )
    order_id:int = order_id[0]
    #Обновление данных в корнизе 
    await update_data_bakcet(session=session_param, user_id=current_user.id, order_id=order_id)
