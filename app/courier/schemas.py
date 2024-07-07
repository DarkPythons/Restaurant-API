from pydantic import BaseModel, Field, EmailStr
from enum import Enum




class BaseCourierSchemas(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=5, max_length=20)    
    verified: bool = Field(default=False)
    in_work: bool = Field(default=False)


class AddNewCourierShemas(BaseCourierSchemas):
    email: EmailStr = Field(min_length=5, max_length=100)

    


class ShowCourierSchemas(BaseCourierSchemas):
    id: int
    user_id: int