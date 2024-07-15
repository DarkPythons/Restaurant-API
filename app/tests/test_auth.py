import pytest
from .conftest import client





def test_register():
    """Тестировка регистрации по правильным параметрам"""
    response = client.post(url="/auth/register", json={
  "email": "user1@example.com",
  "password": "string",
  "is_active": True,
  "is_superuser": False,
  "is_verified": False,
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}
    )
    assert response.status_code in [200, 201]

def test_login():
    """Выполнение входа по правильным параметрам"""
    response = client.post(url="/auth/login", data={"username" : "user1@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys

def test_logout():
    """Выполнение выхода по правильным куки"""
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/auth/logout", cookies=cookies)
    assert  response.status_code == 204
    assert not response.cookies

def test_bad_register():
    """Тестировка регистрации с повторяющимся email"""
    response = client.post(url="/auth/register",json={
  "email": "user1@example.com",
  "password": "string",
  "is_active": True,
  "is_superuser": False,
  "is_verified": False,
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}
    )
    assert response.status_code == 400
    assert response.json()['detail'] == "REGISTER_USER_ALREADY_EXISTS"

def test_bad_register_validatre():
    """Тестировка, если неправильно введено значение"""
    response = client.post(url="/auth/register",json={
  "email": "user1@example.com",
  "password": "string",
  "is_active": True,
  "is_superuser": False,
  "is_verified": "false",
  "first_name": "string",
  "last_name": "string",
}
    )

    assert response.status_code == 422

def test_bad_login():
    """Тестировка входа, если пользователя нет"""
    response = client.post(url="/auth/login", data={"username" : "us@example.com", "password" : 'stringdsf'})
    assert response.status_code == 400
    assert response.json()['detail'] == 'LOGIN_BAD_CREDENTIALS'

def test_bad_login_valid():
    """Тестировка входа, если данные не правильные"""
    response = client.post(url="/auth/login", data={"username" : "us@example.com", "password" : False})
    assert response.status_code == 400

def test_bad_logout():
    """Тестировка выхода, если человек не был в аккаунте"""
    response = client.post(url="/auth/logout")
    assert  response.status_code == 401
    assert response.json()['detail'] == "Unauthorized"
def test_bad_logunt_cookie():
    """Тестировка выхода, если неправильные куки"""
    cookies = {'authenticate_user' : "bad_cookie"}
    response = client.post(url="/auth/logout", cookies=cookies)
    assert response.status_code == 401
    assert response.json()['detail'] == "Unauthorized" 