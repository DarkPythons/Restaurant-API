from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas,exceptions,FastAPIUsers
from config import SettingsForTokenJWT
from typing import Optional,Annotated
from fastapi import Depends, Request

from auth.models import User
from auth.auth import auth_backend
from database import get_user_db

settings_for_token = SettingsForTokenJWT()
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    #Переопределение переменных класса BaseUserManager для правильной работы
    reset_password_token_secret = settings_for_token.AUTH_SECRET_TOKEN_JWT
    verification_token_secret = settings_for_token.AUTH_SECRET_TOKEN_JWT

    #Переопределение метода (что будет происходить после регистрации пользователя)
    async def on_after_register(self, user: User, request: Optional[Request]):
        print(f'User: {user.id}, has register!!!')
    
    #Полное переопределение метода (метод для создания пользователя в базе данных)
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        #Берем пароль из словаря
        password = user_dict.pop("password")
        #переопределяем пароль в конечный dict (только уже хешированный)
        user_dict["hashed_password"] = self.password_helper.hash(password)
        created_user = await self.user_db.create(user_dict)

        

        await self.on_after_register(created_user, request)

        return created_user

#Возвраение мэнэджера для работы с юзером
async def get_user_managers(user_db: Annotated[User, Depends(get_user_db)]):
    yield UserManager(user_db)

#Модель человека 
fastapi_users_modules = FastAPIUsers[User, int](get_user_managers, [auth_backend],)