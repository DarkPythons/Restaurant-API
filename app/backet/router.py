from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from auth.models import User
from typing import Annotated
from .orm import *
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from fastapi.responses import ORJSONResponse
router_backet = APIRouter()

@router_backet.post('/add_new_item_for_backet/{item_id}')
async def add_new_item_for_backet(current_user: Annotated[User, Depends(get_current_user)], item_id:int, session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    list_id_for_items_menu:list = await get_list_id_items(session=session_param)
    if item_id in  list_id_for_items_menu:
        await add_new_item_for_backet_orm(user_id=current_user.id, item_id=item_id, session=session_param, order_id=None)
        return ORJSONResponse(status_code=201, content={'content' : 'Вы успешно добавили новый предмет в корзину'}) 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Предмета с таким айди не найдено')

@router_backet.get('/get_my_backet/')
async def get_backet_for_user(current_user: Annotated[User, Depends(get_current_user)],session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    items_for_backet = await get_raw_info_for_table(session=session_param, user_id=current_user.id)
    if items_for_backet:
        itog_list: list = []
        for one_item_for_bakcet in items_for_backet:
            #Данные каждого элемента в корзине
            data:list = {}
            data['metainfo'] = {'user_id' : one_item_for_bakcet['user_id'], "item_id" :  one_item_for_bakcet['item_id'], 'order_id' : one_item_for_bakcet['order_id']}
            #Добавление информации об самом item
            item_info_orm = await get_info_for_orm(session=session_param, item_id=one_item_for_bakcet['item_id'])
            item_info_orm = item_info_orm[0]
            data['item_info'] = []
            data['item_info'].append(item_info_orm)
            itog_list.append(data)
        return itog_list
            
    else:
        return ORJSONResponse(status_code=200, content={'content' : []}) 

