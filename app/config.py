from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr
from dotenv import load_dotenv, find_dotenv
import os

#Подгрузка значений из окружения
load_dotenv(find_dotenv())

class BaseConfigClassInFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8', 
        #Чувствительность к регистру
        case_sensitive=True,
    )



class BaseSettingForApp(BaseConfigClassInFile):
    NAME_APP: str = Field(min_length=1, max_length=30, default='SuperApp')
    VERSION_APP: str = Field(default="0.0.1")


class DataBaseSettingPostgre(BaseConfigClassInFile):
    #Данные в default представлены в виде примера
    DB_USER:str = Field(min_length=1, max_length=30, default="postgres")
    DB_PASS:str = Field(min_length=5, max_length=100)
    DB_HOST:str = Field(min_length=1, max_length=15, default='127.0.0.1')
    DB_PORT:str = Field(min_length=1, max_length=10, default='5432')
    DB_NAME:str = Field(min_length=1, max_length=100, default='praktika_fastapi')



class SettingsForTokenJWT(BaseConfigClassInFile):
    AUTH_SECRET_TOKEN_JWT:str = Field(min_length=1, max_length=150)
    TIME_FOR_LIFE_TOKEN:int=Field(ge=10, le=3600000, default=3600)


class BaseSettingsConfig(BaseConfigClassInFile):
    PROJECT_IS_PROCESS_DEBUG: bool = Field(default=True)
    HTTP_OR_HTTPS: str = Field(default='http')

class RassilkaBaseConfig(BaseConfigClassInFile):
    RASSILKA_IN_EMAIL: bool = Field(default=False)

class CeleryConfigSettings(BaseConfigClassInFile):
    SMTP_USER:EmailStr = Field()
    SMTP_PASSWORD:str = Field(default='password')
    SMTP_HOST:str=Field(default='smtp.gmail.com')
    SMTP_PORT:int=Field(default=465)

#В default указаны настройки для локального включения, на сервере они будут совсем другие
class RedisConfigSettings(BaseConfigClassInFile):
    REDIS_HOST:str=Field(default='localhost')
    REDIS_PORT:int=Field(default=6379)

#Параметры базы данных для тестировки приложения
class TestingAppDatabaseSettings(BaseConfigClassInFile):
    DB_HOST_TEST:str = Field(min_length=1, max_length=15, default='127.0.0.1')
    DB_PORT_TEST:str = Field(min_length=1, max_length=10, default='5432')
    DB_PASS_TEST:str = Field(min_length=5, max_length=100)
    DB_NAME_TEST:str = Field(min_length=1, max_length=100, default='praktika_fastapi_test')
    DB_USER_TEST:str = Field(min_length=1, max_length=30, default="postgres")


description = """
## Это API приложение, которое может показать некоторую структуру приложения по доставке еды.
## Вы можете попробывать выполнить разные операции с этим API, используя эту документацию, или внешние приложения
### Это API может:
* **Добавлять рестораны и их информацию в базу данных**
* **При аунтефикации пользователь получает доступ к корзине, которая тоже связана с базой**
* **Пользователь может заказать предметы из своей корзины**
* **Если человек имеет права супер пользователя, он может добавлять курьеров**
* **Эти курьеры могут просматривать и брать заказаы, которые делают пользователи**
## **Это API не является enterprise версией, тут нет платежей, проверок, и тд.**
"""

tags_metadata = [
    {
        'name' : 'Auth',
        'description' : 'Список API для аунтефикации, регистрации и выхода, после регистрации пройдите аунтефикацию - **/login**',
    },
    {
        'name' : 'Restoraunt',
        'description' : 'Список API для взаимодействия с рестораном, вы можете добавлять \
        ресторан, смотреть по нему информацию, **и многое другое**'
    },
    {
        'name' : 'Courier',
        'description' : 'Список API для курьеров, если супер пользователь выдаст вам права курьера, \
        вы сможете брать заказы, смотреть их, и менять их статус'
    },
    {
        'name' : 'Backet',
        'description' : 'Список API для обычных пользоватей, которые хотят брать, удалять, просматривать свои **добавленные товары**'
    },
    {
        'name' : 'Order',
        'description' : 'Список API для взаимодействия с заказами, которые были сделаны пользователем'
    }    
]