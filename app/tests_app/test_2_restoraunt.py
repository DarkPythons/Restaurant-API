import pytest
from .conftest import client


def test_regitser_rest():
    response = client.post(url="/auth/register", json={
  "email": "restor@example.com",
  "password": "string",
  "is_active": True,
  "is_superuser": False,
  "is_verified": False,
  "first_name": "Shef",
  "last_name": "Povar",
  "phone": "+78888888888"
}
    )
    assert response.status_code in [200, 201]

def test_login_rest():
    response = client.post(url="/auth/login", data={"username" : "restor@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys

def test_create_restorunt():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/create_new_restoraunt/", cookies=cookies, json={
  "title": "Super Restoraunt",
  "rating": 5,
  "address": "Филадельфия 42",
  "description": "Самый лучий прекрасный ресторан"
})
    assert response.status_code == 201
    assert response.json()['content'] == "Ресторан с названием Super Restoraunt успешно добавлен в базу!"

def test_bad_create_restoraunt():
    """Тест, на попытку создать ресторан с плохими cookie"""
    cookies = {'authenticate_user' : "bad_cookie"}
    response = client.post(url="/restoraunt/create_new_restoraunt/", cookies=cookies, json={
  "title": "Super Restoraunt",
  "rating": 5,
  "address": "Филадельфия 42",
  "description": "Самый лучий прекрасный ресторан"
})
    assert response.status_code == 401
    assert response.json()['detail'] == "Unauthorized"

def test_bad_valide_create_rest():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/create_new_restoraunt/", cookies=cookies, json={
  "title": "Super Restoraunt",
  "rating": 5,
  "address": "Филадельфия 42",
  "description": False
})
    assert response.status_code == 422


def test_add_basemnenu():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_menu_baseinfo/1", cookies=cookies, json={
  "title": "Супер лучшее меню",
  "description": "Меню состоит из множества категорий на любой ваш выбор"
})
    assert response.status_code == 201
    assert response.json()['content'] == "Создание объекта меню произошло успешно!"

def test_add_bad_basemen():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_menu_baseinfo/5", cookies=cookies, json={
  "title": "Супер лучшее меню",
  "description": "super restorunt menu"
})
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким id не найдено."

def test_add_new_category():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_category/1/1", cookies=cookies, json={
  "title": "Морепродукты",
  "description": "Самая вкусная категория в меню"
})
    assert response.status_code == 201
    assert response.json()['content'] == "Создаение категории произошло успешно!"

def test_bad_add_new_category1():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_category/1/2", cookies=cookies, json={
  "title": "Морепродукты",
  "description": "Самая вкусная категория в меню"
})
    assert response.status_code == 404
    assert response.json()['detail'] == "У данного ресторана не такой menu_id."

def test_bad_add_new_category2():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_category/2/1", cookies=cookies, json={
  "title": "Морепродукты",
  "description": "Самая вкусная категория в меню"
})
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким id не найдено."

def test_add_new_dishes():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_dishaes/1/1/1/", cookies=cookies, json=[
  {
    "title": "Рыбка под соусом",
    "description": "Самая вкусная рыба в мире",
    "price": 100,
    "sostav": "Крупа кукурузная, рыба, яблоко",
    "kolories": 20
  }
])
    assert response.status_code == 201
    assert response.json()['content'] == "Занесение блюда в меню произошло успешно!"

def test_bad_new_dishes1():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_dishaes/2/1/1/", cookies=cookies, json=[
  {
    "title": "Рыбка под соусом",
    "description": "Самая вкусная рыба в мире",
    "price": 100,
    "sostav": "Крупа кукурузная, рыба, яблоко",
    "kolories": 20
  }
])
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким id не найдено."

def test_bad_new_dishes2():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_dishaes/1/2/1/", cookies=cookies, json=[
  {
    "title": "Рыбка под соусом",
    "description": "Самая вкусная рыба в мире",
    "price": 100,
    "sostav": "Крупа кукурузная, рыба, яблоко",
    "kolories": 20
  }
])
    assert response.status_code == 404
    assert response.json()['detail'] == "Меню с таким айди у этого ресторана нет."

def test_bad_new_dishes2():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_new_dishaes/1/1/2/", cookies=cookies, json=[
  {
    "title": "Рыбка под соусом",
    "description": "Самая вкусная рыба в мире",
    "price": 100,
    "sostav": "Крупа кукурузная, рыба, яблоко",
    "kolories": 20
  }
])
    assert response.status_code == 404
    assert response.json()['detail'] == "Категории с таким id в данном меню не найдено."

def test_add_contact_info():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_contact_info/1/", cookies=cookies, json={
  "phone": "+79999999999",
  "manager": "Петров Петрович",
  "office_restoraunt_address": "Филадельфия 20"
})
    assert response.status_code == 201
    assert response.json()['content'] == "Добавление контактной информации успешно произошло!"

def test_bad_add_contact_info():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/restoraunt/add_contact_info/2/", cookies=cookies, json={
  "phone": "+79999999999",
  "manager": "Петров Петрович",
  "office_restoraunt_address": "Филадельфия 20"
})
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким id не найдено."

json_data = {
  "base_restoraunt_info": {
    "title": "Super Restoraunt",
    "rating": 5,
    "address": "Филадельфия 42",
    "description": "Самый лучий прекрасный ресторан",
    "id": 1
  },
  "contact_information": {
    "id": 1,
    "phone": "+79999999999",
    "manager": "Петров Петрович",
    "office_restoraunt_address": "Филадельфия 20",
    "restoraunt_id": 1
  },
  "base_menu_info": {
    "title": "Супер лучшее меню",
    "description": "Меню состоит из множества категорий на любой ваш выбор",
    "id": 1,
    "restoraunt_id": 1
  },
  "menu_list": [
    {
      "Морепродукты": [
        {
          "id": 1,
          "title": "Рыбка под соусом",
          "description": "Самая вкусная рыба в мире",
          "price": 100,
          "sostav": "Крупа кукурузная, рыба, яблоко",
          "kolories": 20,
          "category_id": 1,
          "menu_id": 1,
          "restoraunt_id": 1
        }
      ]
    }
  ]
}


def test_get_info_for_rest_by_id():
    response = client.get(url="/restoraunt/get_info_restoraunt/1")
    assert response.status_code == 200
    assert response.json()  == 	json_data
    
def test_get_info_by_title():
    response = client.get(url="/restoraunt/get_info_for_restoaunt/Super Restoraunt")
    assert response.status_code == 200
    assert response.json() == json_data

def test_bad_info_by_id():
    response = client.get(url="/restoraunt/get_info_for_restoaunt/Not rest")
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким названием нет"

def test_bad_info_by_id():
    response = client.get(url="/restoraunt/get_info_restoraunt/5")
    assert response.status_code == 404
    assert response.json()['detail'] == "Ресторана с таким id нет"