from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from config import SettingsForTokenJWT

settings_for_token = SettingsForTokenJWT()

cookie_transport = CookieTransport(cookie_max_age=settings_for_token.TIME_FOR_LIFE_TOKEN, cookie_name='authenticate_user')

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings_for_token.AUTH_SECRET_TOKEN_JWT, lifetime_seconds=settings_for_token.TIME_FOR_LIFE_TOKEN)


#Модель авторизации (название модели, параметры куки, стретегия(какая технология и как работает))
auth_backend = AuthenticationBackend(name='jwt', transport=cookie_transport, get_strategy=get_jwt_strategy)