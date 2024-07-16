from fastapi import FastAPI, Request
from config import BaseSettingForApp
from contextlib import asynccontextmanager
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
import time

from config import BaseSettingForApp, BaseSettingsConfig, description, tags_metadata
from database import create_table, delete_table
from auth.models import User
from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.schema import UserCreate, UserRead
from restoraunt.routers import router as restoraunt_router
from courier.routers import router_courier
from backet.router import router_backet
from orders.routers import router_order
from baselog import custom_log_app,custom_log_exception



settings_app = BaseSettingForApp()
conifgs_app = BaseSettingsConfig()



@asynccontextmanager
async def lifespan_for_fastapi(app:FastAPI):
    try:    
        await create_table()
    except Exception as Error:
        custom_log_exception.error(f"Возникла ошибка при создании таблиц, описание: {Error}")
    custom_log_app.info(f"Приложение было включено.")
    yield
    #Действия после выключения приложения
    try:
        #Если проект в режиме разработки, после работы удалить все таблицы:
        if conifgs_app.PROJECT_IS_PROCESS_DEBUG:
            await delete_table()
    except Exception as Error:
        custom_log_exception.error(f"Возникла ошибка при удалении таблиц, описание: {Error}")
    custom_log_app.info(f"Приложение было выключено.")





app = FastAPI(
    title=settings_app.NAME_APP,
    version=settings_app.VERSION_APP,
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=lifespan_for_fastapi,
    description=description,
    summary='API приложения по доставке еды',
    contact={
        #Кастомные настройки контактов
        "name" : 'Creator',
        'url' : 'https://github.com/VoblaSuperFish',
    },
    license_info={
        #Информация об подключенных лицензиях
        'name' : 'MIT Licenses',
        'url' : 'https://mit-license.org/'
    },
    openapi_tags=tags_metadata,
    #Изменение подсветки синтаксиса
    swagger_ui_parameters={'syntaxHighlight.theme' : 'obsidian'}
)


app.include_router(
    restoraunt_router,
    prefix='/restoraunt',
    tags=['Restoraunt']
    )

app.include_router(
    router_courier,
    prefix='/courier',
    tags=['Courier']
)

app.include_router(
    router_backet,
    prefix='/backet',
    tags=['Backet']
)

app.include_router(
    router_order,
    prefix='/orders',
    tags=['Order']
)



app.add_middleware(
    CORSMiddleware,
    #Разрешенные хоста, которые могут обращаться к API
    allow_origins=['*'],
    #Использование файлов Cookie и Authorization
    allow_credentials=True,
    #Разрашенные методы которые могут поступать с разрашенных хостов
    allow_methods=['*'],
    #Разрашенные заголовки
    allow_headers=['*'],
)

fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

#ручка для аунтефикации пользовател, также нужно указать auth_backend (модель что выдавать юзеру, в нашем случае JWT) 
app.include_router(fastapi_users_modules.get_auth_router(auth_backend), prefix='/auth', tags=['Auth'])
#Добавление ручки для регистрации
app.include_router(fastapi_users_modules.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['Auth'])



#Добалвение middleware, который перехватывает запросы http/https и добавляет к ним время выполнения операции
@app.middleware(conifgs_app.HTTP_OR_HTTPS)
async def add_time_process_in_header(request: Request, call_next):
    start_time = time.time()
    #Вызов функции к которой шёл запрос с параметрами
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)

    
    #Получить хост и порт обратившегося человека
    client_host = request.client.host
    client_port = request.client.port
    custom_log_app.info(f"Пользователь с хостом {client_host} и портом {client_port} обратился к API, время: {str(process_time)}")
    return response