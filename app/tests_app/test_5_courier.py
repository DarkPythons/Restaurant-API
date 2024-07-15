import pytest, pytest_asyncio
from .conftest import client, async_session_maker
from sqlalchemy import insert, select, update
from auth.models import user


    

@pytest_asyncio.fixture(autouse=True, scope="session")
async def new_admin():
    async with async_session_maker() as session:
        query = update(user).values(is_superuser=True).where(user.c.email == "restor@example.com")
        await session.execute(query)
        await session.commit()

def test_login_rest():
    response = client.post(url="/auth/login", data={"username" : "restor@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys


def test_add_new_courier():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/courier/add_new_courier/1",cookies=cookies, json={
  "first_name": "Николай",
  "last_name": "Николаич",
  "phone": "+77777777777",
  "verified": False,
  "in_work": False,
  "email": "user1@example.com"
})
    assert response.status_code == 201
    assert response.json()['content'] == "Пользователь Николай Николаич, с айди 1 был добавлен в таблицу курьеров"

def test_bad_get_my_active_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get('/courier/get_my_active_order/', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете взять заказ."

def test_bad_get_info_account():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get('/courier/get_info_account', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете получить информацию об аккаунте курьерa."

def test_bad_get_orders_all():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get('/courier/get_orders_all/', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете получать информацию об свободных заказах."

def test_bad_update_status_work():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post('/courier/update_my_status_work/?in_work=true', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете обновлять статус работы."

def test_bad_verifed_profile():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post('/courier/verified_my_courier_account/', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете получить верификацию для курьеров."

def test_bad_take_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post('/courier/take_order/1', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете взять заказ."

def test_bad_update_status_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.put('/courier/update_status_order/1?new_status=Готовится', cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Вы не являетесь курьером, поэтому не можете обновлять статус заказа"

def test_logout():
    """Выполнение выхода по правильным куки"""
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/auth/logout", cookies=cookies)
    assert  response.status_code == 204
    assert not response.cookies

def test_login():
    """Выполнение входа по правильным параметрам (Вход в аккаунт курьера)"""
    response = client.post(url="/auth/login", data={"username" : "user1@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys


def test_get_my_active_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get(url="/courier/get_my_active_order/", cookies = cookies)

    assert response.status_code == 200
    assert response.json() == []

def test_get_my_info_account():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get(url="/courier/get_info_account", cookies = cookies)
    assert response.status_code == 200
    assert response.json() == {
  "account_info": {
    "first_name": "Николай",
    "last_name": "Николаич",
    "phone": "+77777777777",
    "in_work": False,
    "verified": False,
    "email": "user1@example.com"
  }
}

def test_get_orders_all():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get(url="/courier/get_orders_all/", cookies = cookies)
    assert response.status_code == 200
    assert response.json() == [
  {
    "id": 1,
    "price_order": 100,
    "status": "Готовится",
    "address": "Филадельфия 2",
    "user_id": 1,
    "courier_id": None
  }
]

def test_update_my_status_work():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/courier/update_my_status_work/?in_work=false", cookies = cookies)
    assert response.status_code == 200
    assert response.json()['content'] == "Ваш статус работы обновлен на: Не в работе"

def test_verified_my_account():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/courier/verified_my_courier_account/", cookies = cookies)
    assert response.status_code == 200
    assert response.json()['content'] == "Ваш статус верификации обновлен"

def test_take_order_my_account():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/courier/take_order/1", cookies = cookies)
    assert response.status_code == 202
    assert response.json()['content'] == "Вы добавили заказ номер 1 к своим заказам, хорошей доставки."

def test_bad_update_status_order_not_found():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.put(url="/courier/update_status_order/5?new_status=Готовится", cookies = cookies)
    assert response.status_code == 404
    assert response.json()['detail'] == "Заказа с таким id нет, или у вас лично нет заказа с таким id"

def test_update_status_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.put(url="/courier/update_status_order/1?new_status=Готовится", cookies = cookies)
    assert response.status_code == 200
    assert response.json()['content'] == "Вы успешно обновили статус заказа."

def test_update_finish_status_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.put(url="/courier/update_status_order/1?new_status=Доставлен", cookies = cookies)
    assert response.status_code == 200
    assert response.json()['content'] == "Вы успешно обновили статус заказа."

def test_bad_update_finish_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.put(url="/courier/update_status_order/1?new_status=Доставлен", cookies = cookies)
    assert response.status_code == 400
    assert response.json()['detail'] == "Вы не можете изменять статус доставленных заказов"