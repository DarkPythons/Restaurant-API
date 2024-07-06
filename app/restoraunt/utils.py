from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User
from .orm import get_restoraunt_osnov_for_id_rest, get_category_orm, get_list_products_for_category
fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()

async def user_is_osvov_restoraunt(*, restoraunt_id, current_user,session):
    restoraunt_user_osnovatel = await get_restoraunt_osnov_for_id_rest(session=session, restoraunt_id=restoraunt_id)
    print(restoraunt_user_osnovatel)
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
        products_list_dict_for_category = await get_list_products_for_category(category_id=one_category_info['id'], session=session)
        products_list_dict_for_category = [dict(x) for x in products_list_dict_for_category]
        dict_category[one_category_info["title"]] = products_list_dict_for_category
        list_category_dishayes.append(dict_category)
    return list_category_dishayes
