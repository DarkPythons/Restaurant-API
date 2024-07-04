from fastapi_users import schemas
from pydantic import EmailStr  
from typing import Optional

#Валидация для чтения человека
class UserRead(schemas.BaseUser[int]):
    #Переопределение параметров от BaseUser
    id: int
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False 
    is_verified: Optional[bool] = False


#Схема валидации при создании
class UserCreate(schemas.BaseUserCreate):
    #Переопределение параметров от BaseUserCreate
    email: EmailStr
    password: str  
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False



