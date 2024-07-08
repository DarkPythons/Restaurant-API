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
        itog_list_data: list = []
        for one_item_for_bakcet in items_for_backet:
            #Данные каждого элемента в корзине
            data:list = {}
            data['metainfo'] = {"backet_id" : one_item_for_bakcet['id'], 'user_id' : one_item_for_bakcet['user_id'], "item_id" :  one_item_for_bakcet['item_id'], 'order_id' : one_item_for_bakcet['order_id']}
            #Добавление информации об самом item
            item_info_orm = await get_info_for_orm(session=session_param, item_id=one_item_for_bakcet['item_id'])
            item_info_orm = item_info_orm[0]
            data['item_info'] = []
            data['item_info'].append(item_info_orm)
            itog_list_data.append(data)
        return itog_list_data
            
    else:
        return ORJSONResponse(status_code=200, content={'content' : []}) 


#Удаление предмета из корзины
@router_backet.delete('/delete_item/{backet_id}')
async def delete_one_item_bakcet(backet_id:int, current_user: Annotated[User, Depends(get_current_user)],session_param: Annotated[AsyncSession, Depends(get_async_session)]):
    backet_item_user:list = await get_info_back_for_id(backet_id=backet_id, session=session_param)
    if backet_item_user:
        backet_item_user:dict = backet_item_user[0]
        if backet_item_user['user_id'] == current_user.id:
            if not backet_item_user['order_id']:
                await delete_item_backet(backet_id=backet_id, session=session_param)
                return ORJSONResponse(status_code=200, content={f'content' : f'Вы успешно удалили элемент корзины с айди: {backet_id}'}) 
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Вы пытается удалить элемент корзины, который есть в действующем заказе.')
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы пытаетесь удалить элемент чужой корзины.')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Вы пытаетесь удалить элемент айди которого нет.')