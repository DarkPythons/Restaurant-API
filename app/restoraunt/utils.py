from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Path
from enum import Enum

from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User
from .orm import (
    get_restoraunt_osnov_for_id_rest, 
    get_category_orm, get_list_products_for_category, 
    get_menu_info_for_orm,
    get_contact_info_orm,get_menu_id_for_restoraunt,
    get_info_restoraunt_by_id
)

class PathParamsDescription(Enum):
    restoraunt_id = Path(title="Айди ресторана", description="Введите айди ресторана:", ge=1)
    menu_id = Path(title='Айди меню', description="Введите айди меню:", ge=1)
    category_id = Path(title='Айди категории', description='Введите айди категории:', ge=1)


fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()

async def user_is_osvov_restoraunt(*, restoraunt_id, current_user,session):
    restoraunt_user_osnovatel = await get_restoraunt_osnov_for_id_rest(
        session=session, restoraunt_id=restoraunt_id
        )
    if restoraunt_user_osnovatel:
        if current_user.id == restoraunt_user_osnovatel[0]:
            return 200
        else:
            return 400
    else:
        return 'Not restoraunt'


async def get_list_products_for_menu(*, restoraunt_id, session):
    category_info_list:list = await get_category_orm(restoraunt_id=restoraunt_id, session=session)
    list_category_dishayes:list = []
    for one_category_info in category_info_list:
        dict_category: dict = {}
        products_list_dict_for_category = await get_list_products_for_category(
            category_id=one_category_info['id'], session=session
        )
        products_list_dict_for_category = [dict(x) for x in products_list_dict_for_category]
        dict_category[one_category_info["title"]] = products_list_dict_for_category
        list_category_dishayes.append(dict_category)
    return list_category_dishayes



async def get_contact_info(*,restoraunt_id:int, session: AsyncSession):
    #Получение контактной информации
    contact_info_itog = {}
    contact_info = await get_contact_info_orm(restoraunt_id=restoraunt_id, session=session)
    if contact_info:
        contact_info_itog = {**contact_info[0]}
    return contact_info_itog

async def get_base_menu_info(restoraunt_id:int,session:AsyncSession):
    base_menu_info = await get_menu_info_for_orm(restoraunt_id=restoraunt_id, session=session)
    if not base_menu_info:
        return {}
    else:
        return base_menu_info[0]

async def get_data_itog_for_restoraunt(restoraunt_id:int, session: AsyncSession, base_result_by_search):
    contact_info = await get_contact_info(restoraunt_id=restoraunt_id, session=session)
    list_category_dishayes = await get_list_products_for_menu(restoraunt_id=restoraunt_id, session=session)
    base_info_restoraunt = {**base_result_by_search[0]}
    base_menu_info = await get_base_menu_info(restoraunt_id=restoraunt_id,session=session)
    data_itog = {
        "base_restoraunt_info" : base_info_restoraunt, 
        "contact_information" : contact_info, 
        'base_menu_info' : base_menu_info, 
        "menu_list" : list_category_dishayes
        }
    return data_itog

async def get_menu_id_func(*, restoraunt_id, session_param):
    try:
        menu_id_for_orm = await get_menu_id_for_restoraunt(restoraunt_id=restoraunt_id, session=session_param)
        menu_id_for_orm = int(menu_id_for_orm[0][0])  
        return menu_id_for_orm
    except:
        raise HTTPException(status_code=404, detail='У данного ресторана пока нет меню.')


async def get_info_title_rest(*,rest_id:int, session: AsyncSession):
    id_for_restoraunt_by_id = rest_id[0]
    base_result_by_search:list = await get_info_restoraunt_by_id(restoraunt_id=id_for_restoraunt_by_id, session=session)
    data_itog = await get_data_itog_for_restoraunt(restoraunt_id=id_for_restoraunt_by_id, session=session, base_result_by_search=base_result_by_search)   
    return data_itog