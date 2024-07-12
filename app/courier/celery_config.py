import smtplib
from celery import Celery
from config import CeleryConfigSettings, RedisConfigSettings
from email.message import EmailMessage

redis_config = RedisConfigSettings()
celery_config = CeleryConfigSettings()
celery_courier_rassilka = Celery('courier', broker=f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}")


def get_template_rassilka_courier(slovar_data):
    email = EmailMessage()
    email['Subject'] = "Рассылка курьерам"
    email['From'] = celery_config.SMTP_USER
    email['To'] = slovar_data['email_courier']

    email.set_content(
        '<div style="font-family: sans-serif;">'
        f'<h2 style="color:aqua">Добрый день, {slovar_data['first_name_courier']} {slovar_data['last_name_courier']},</h2>'
        f'<p>Вы доставили заказ по адресу {slovar_data['address_order']}, за что, наша компания очень вам признательна,</p>'
        f'<p style="color:red;">Информация по заказу:</p>'
        f'<ul>Стоимость: {slovar_data['price_order']}</ul>'
        f"<ul>Конечный адрес: {slovar_data['address_order']}</ul>"
        f"<ul>Айди заказа: {slovar_data['order_id']}</ul>"
        f"<ul>Айди заказчика: {slovar_data['user_id']}</ul>"
        '<h2 style="color:aqua">Если у вас остались вопросы, обращайтесь в поддержку.</h2>'
        "<h3>Хорошего вам дня</h3>"
        "<img src='https://img.freepik.com/free-photo/man-delivering-groceries-customers_23-2149950082.jpg?t=st=1720799275~exp=1720802875~hmac=809cb8a16135b32bf721ee19cefae22b1d49b0989ab9f464ba5d2f436b7edeaa&w=996' width='600'>"
        "</div>",
        subtype="html"
    )
    return email


@celery_courier_rassilka.task
def send_email_message_courier(slovar_data):
    with smtplib.SMTP_SSL(celery_config.SMTP_HOST, celery_config.SMTP_PORT) as server:
        server.login(celery_config.SMTP_USER, celery_config.SMTP_PASSWORD)
        email_template = get_template_rassilka_courier(slovar_data)
        server.send_message(email_template)
        