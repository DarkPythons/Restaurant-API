from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from auth.models import User
from typing import Annotated
from .schemas import AddNewCourierShemas
router_courier = APIRouter()

@router_courier.post('/add_new_courier/{user_id}')
async def add_new_courier(user_id:int, current_user: Annotated[User, Depends(get_current_user)], info_for_courier_add: AddNewCourierShemas):
    if current_user.is_superuser:
        return info_for_courier_add
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У вас нет прав на добавление курьеров.')