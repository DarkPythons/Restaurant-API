from fastapi import FastAPI
from config import BaseSettingForApp
from contextlib import asynccontextmanager
from config import PROJECT_IS_PROCESS_DEBUG
from database import create_table, delete_table
from fastapi_users import FastAPIUsers
from auth.models import User
from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.schema import UserCreate, UserRead
from restoraunt.routers import router as restoraunt_router
settings_app = BaseSettingForApp()


@asynccontextmanager
async def lifespan_for_fastapi(app:FastAPI):
    #действия после запуска
    try:    
        await create_table()
    except:
        print('Таблицы уже созданы, можете начинать работу!')
    yield
    #Действия после выключения приложения
    #Если проект в режиме разработки, после работы удалить все таблицы:
    if PROJECT_IS_PROCESS_DEBUG:
        await delete_table()




app = FastAPI(
    title=settings_app.NAME_APP,
    version=settings_app.VERSION_APP,
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=lifespan_for_fastapi
)


app.include_router(
    restoraunt_router,
    prefix='/restoraunt',
    tags=['Restoraunt']
    )


fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

#Фукнция для аунтефикации пользовател, также нужно указать auth_backend (модель что выдавать юзеру, в нашем случае JWT) 
app.include_router(fastapi_users_modules.get_auth_router(auth_backend), prefix='/auth', tags=['Auth'])
#Функция для Регистрации и получения информации по юзеру
app.include_router(fastapi_users_modules.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['Auth'])
#Функция для получения корректного юзера


