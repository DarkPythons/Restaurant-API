from pydantic import BaseModel, Field
from typing import Optional, List


#Схема для блюда
class BaseDishesSchema(BaseModel):
    title:str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None) 
    price: int = Field(ge=0.0)
    sostav: str = Field(min_length=10, max_length=500)
    kolories: Optional[int] = Field(ge=0.0,default=None)

class AddDishiesSchema(BaseDishesSchema):
    pass

class GetDishiesSchema(BaseDishesSchema):
    id: int



#Категория продукта
class CategorySchema(BaseModel):
    title:str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)

class BaseCategorySchema(BaseModel):
    title:str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)

class AddNewCategorSchema(BaseCategorySchema):
    pass




class ShowCategorySchema(CategorySchema):
    dishes_from_the_category: List[AddDishiesSchema]






class ContatSchema(BaseModel):
    phone: str
    manager: Optional[str] = Field(min_length=3, max_length=200, default=None)
    office_restoraunt_address: Optional[str] = None


class BaseRestorauntSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    rating: float = Field(ge=0.0, le=5.0, default=0.0)
    address: str = Field(min_length=5, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)

    


class AddNewRestoraunt(BaseRestorauntSchema):
    pass

class BaseMenuRestoraunt(BaseModel):
    title:str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)    


class AddMenuSchema(BaseMenuRestoraunt):
    pass

class ShowMenuSchema(BaseMenuRestoraunt):
    cetegotiers_list: List[CategorySchema]




class ShowInfoRestoraunt(BaseRestorauntSchema):
    #Айди ресторана из базы
    id: int  
    contact_information: ContatSchema
    #Глубокая вложенность для меню
    menu: Optional[ShowMenuSchema] = None