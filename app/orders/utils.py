from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_managers
from auth.models import User

fastapi_users_modules = FastAPIUsers[User, int](
    get_user_manager=get_user_managers,
    auth_backends=[auth_backend]
)

get_current_user = fastapi_users_modules.current_user()
