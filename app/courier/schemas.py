from pydantic import BaseModel, Field, EmailStr
from fastapi import Query

from orders.schemas import StatusForOrder

class BaseCourierSchemas(BaseModel):
    """Базовая модель для наследования"""
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=5, max_length=20)    
    verified: bool = Field(default=False)
    in_work: bool = Field(default=False)

class AddNewCourierShemas(BaseCourierSchemas):
    """Модель для добавления нового курьера"""
    email: EmailStr = Field(min_length=5, max_length=100)

class ShowCourierSchemas(BaseCourierSchemas):
    """Модель для просмотра информации о курьере из базы"""
    id: int
    user_id: int

class SelectStatus(BaseModel):
    """Модель для выборки состояния заказа"""
    new_status: StatusForOrder = Field(Query())