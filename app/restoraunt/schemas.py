from pydantic import BaseModel, Field
from typing import Optional, List, Dict


#Схемы для блюда
class BaseDishesSchema(BaseModel):
    """базовая pydantic модель для наследования"""
    title:str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None) 
    price: int = Field(ge=0.0)
    sostav: str = Field(min_length=10, max_length=500)
    kolories: Optional[int] = Field(ge=0.0,default=None)
class AddDishiesSchema(BaseDishesSchema):
    """pydantic модель для добавление новых блюд в меню"""
    pass
class GetDishiesSchema(BaseDishesSchema):
    """pydantic модель для получения блюда из базы данных"""
    id: int
    category_id: int
class ListGetDishiesSchema(BaseModel):
    data: List[GetDishiesSchema]



#Схемы для категорий продукта
class BaseCategorySchema(BaseModel):
    """Базовая модель для наследования"""
    title:str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)
class AddNewCategorSchema(BaseCategorySchema):
    """Модель для добавление новой категории в меню"""
    pass
class ShowCategorySchema(BaseCategorySchema):
    """Модель для отображения информации по категории"""
    dishes_from_the_category: List[AddDishiesSchema]

#Схемы для контакной информации
class ContatSchema(BaseModel):
    """Базовая модель для наследования"""
    phone: str
    manager: Optional[str] = Field(min_length=3, max_length=200, default=None)
    office_restoraunt_address: Optional[str] = None

class AddContantSchema(ContatSchema):
    """Модель для создания контактной информации"""
    pass

#Схемы для ресторана
class BaseRestorauntSchema(BaseModel):
    """Модель для наследования"""
    title: str = Field(min_length=1, max_length=50)
    rating: float = Field(ge=0.0, le=5.0, default=0.0)
    address: str = Field(min_length=5, max_length=100)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None)

class AddNewRestoraunt(BaseRestorauntSchema):
    """Модель для создания (добавления) ресторана"""
    pass



#Схемы для меню
class BaseMenuRestoraunt(BaseModel):
    """Модель для наследования"""
    title:str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None) 

class AddMenuSchema(BaseMenuRestoraunt):
    """Модел для добавления базовой информации по меню"""
    pass

#Схемы для просмотра полной инфомрации по ресторану
class ShowBaseInfoRestrount(BaseRestorauntSchema):
    id: int

class VievContantModelNoError(BaseModel):
    """Схема для просмотра контактной информации"""
    id: Optional[int] = Field(default=None)
    phone: Optional[str] = Field(default=None, min_length=5, max_length=20)
    manager: Optional[str] = Field(min_length=3, max_length=200, default=None)
    office_restoraunt_address: Optional[str] = None

    restoraunt_id: Optional[int] = Field(default=None, ge=1)

class BaseMenuInfoNoError(BaseModel):
    """Схема для получения базовой информации по меню"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(min_length=10, max_length=300, default=None) 
    id: Optional[int] = Field(default=None, ge=1)
    restoraunt_id: Optional[int] = Field(default=None, ge=1)

class ShowFullInfoRestoraunt(BaseModel):
    """Схема для просмотра полной информации по ресторану"""
    base_restoraunt_info: ShowBaseInfoRestrount
    contact_information: VievContantModelNoError
    base_menu_info: BaseMenuInfoNoError
    menu_list: List[Dict] 