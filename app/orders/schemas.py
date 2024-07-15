from pydantic import BaseModel, Field
from enum import Enum
from typing import List

class StatusForOrder(Enum):
    """Создание перечисления для выборки курьером статуса заказа"""
    cooking = 'Готовится'
    delivered = 'Доставляется'
    delivered_finish = 'Доставлен'




class BaseShemasOrder(BaseModel):
    """Базовая модель для наследования"""
    price_order: float = Field(ge=1)
    status: StatusForOrder = Field(default=StatusForOrder.cooking)
    address: str = Field(min_length=5, max_length=100)


class AddShemasOrder(BaseShemasOrder):
    """Модель для добавления новых заказов"""
    pass

