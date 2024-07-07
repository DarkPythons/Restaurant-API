from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class StatusForOrder(Enum):
    cooking = 'Готовится'
    delivered = 'Доставляется'
    delivered_finish = 'Доставлен'




class BaseShemasOrder(BaseModel):
    price_order: float = Field(ge=1)
    status: StatusForOrder = Field(default=StatusForOrder.cooking)
    address: str = Field(min_length=5, max_length=100)


class AddShemasOrder(BaseShemasOrder):
    pass


