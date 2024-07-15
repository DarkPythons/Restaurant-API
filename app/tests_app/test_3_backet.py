import pytest
from .conftest import client

def test_login():
    """Выполнение входа по правильным параметрам"""
    response = client.post(url="/auth/login", data={"username" : "user1@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys

def test_get_my_backet():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get("/backet/get_my_backet/", cookies=cookies)

    assert response.status_code == 200
    assert response.json()["content"] == []

def test_bad_take_item():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/backet/add_new_item_for_backet/5", cookies=cookies)

    assert response.status_code == 404
    assert response.json()['detail'] == "Предмета с таким айди не найдено"
  
    response2 = client.get("/backet/get_my_backet/", cookies=cookies)
    assert response2.status_code == 200
    assert response2.json()['content'] == []


def test_take_item():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/backet/add_new_item_for_backet/1", cookies=cookies)

    assert response.status_code == 201
    assert response.json()['content'] == "Вы успешно добавили новый предмет в корзину"

    response2 = client.get("/backet/get_my_backet/", cookies=cookies)

    assert response2.status_code == 200
    assert response2.json() == [
  {
    "metainfo": {
      "backet_id": 1,
      "user_id": 1,
      "item_id": 1,
      "order_id": None
    },
    "item_info": [
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


def test_delete_item_from_backet():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.delete("/backet/delete_item/1", cookies=cookies)

    assert response.status_code == 200
    assert response.json()['content'] == "Вы успешно удалили элемент корзины с айди: 1"

    response2 = client.get("/backet/get_my_backet/", cookies=cookies)
    assert response2.status_code == 200
    assert response2.json()['content'] == []


def test_bad_delete_item_from_backet():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.delete("/backet/delete_item/436", cookies=cookies)

    assert response.status_code == 404
    assert response.json()['detail'] == "Вы пытаетесь удалить элемент, айди которого нет."

