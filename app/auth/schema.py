from fastapi_users import schemas
from pydantic import EmailStr , Field
from typing import Optional

#Валидация для чтения человека
class UserRead(schemas.BaseUser[int]):
    #Кастомные параметры
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=5, max_length=20)    

    #Переопределение параметров от BaseUser
    id: int
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False 
    is_verified: Optional[bool] = False




#Схема валидации при создании
class UserCreate(schemas.BaseUserCreate):
    #Кастомные параметры
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=5, max_length=20)   

    #Переопределение параметров от BaseUserCreate
    email: EmailStr
    password: str  
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

 



