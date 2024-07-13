from loguru import logger
from fastapi import HTTPException, status

class BaseLoggings:
    def __init__(self, *, format:str="{time} {level} {message}",file:str, rotation:str, level:str, serialize:bool=False):
        logger.add(file, format=format, level=level, rotation=rotation, compression="zip", serialize=serialize)

    def debug(self, message):
        logger.debug(message)
    def info(self, message):
        logger.info(message)
    def warning(self, message):
        logger.warning(message)
    def error(self, message):
        logger.error(message)
    def critical(self, message):
        logger.critical(message)

#Логи где будет вся информация
custom_log_app = BaseLoggings(file="../loggs_app/info_app.log", rotation="100 MB", level='DEBUG')
#Логи где будет только информация об ошибках
custom_log_exception = BaseLoggings(file="../loggs_app/except_app.log", rotation="100 MB", level='ERROR')


#Генерация ответа в случае ошибки
async def generate_response_error(Error):
    custom_log_exception.error(Error)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка на стороне сервера")