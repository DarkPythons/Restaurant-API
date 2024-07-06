from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


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
    category_id: int

class ListGetDishiesSchema(BaseModel):
    data: List[GetDishiesSchema]


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

class VievContantModel(ContatSchema):
    id: int
    restoraunt_id: int

class BaseRestorauntSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    rating: float = Field(ge=0.0, le=5.0, default=0.0)
    address: str = Field(min_length=5, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)





class BaseMenuRestoraunt(BaseModel):
    title:str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None) 


class BaseMenuInfo(BaseMenuRestoraunt):
    id: int
    restoraunt_id:int


class ShowMenuSchema(BaseMenuRestoraunt):
    cetegotiers_list: List[CategorySchema]

class ShowBaseInfoRestrount(BaseRestorauntSchema):
    id: int


class SchemaShowCategory(BaseModel):
    category_name: List[Optional[GetDishiesSchema]]


    
class AddNewRestoraunt(BaseRestorauntSchema):
    pass
class AddMenuSchema(BaseMenuRestoraunt):
    pass





class ShowFullInfoRestoraunt(BaseModel):
    base_restoraunt_info: ShowBaseInfoRestrount
    contact_information: VievContantModel
    base_menu_info: BaseMenuInfo
    #Глубокая вложенность для меню
    menu_list: List[Dict]