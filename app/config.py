from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
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
