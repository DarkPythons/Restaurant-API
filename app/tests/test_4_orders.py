import pytest
from .conftest import client
from typing import Any
def test_get_my_active_orders():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get("/orders/view_my_active_order/",cookies=cookies)

    assert response.status_code == 200
    assert response.json()['active_order'] == []

def test_bad_my_active_orders():
    cookies = {'authenticate_user' : "Bad token"}
    response = client.get("/orders/view_my_active_order/",cookies=cookies)
    assert  response.status_code == 401
    assert response.json()['detail'] == "Unauthorized"

def test_bad_view_full_info_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.get("/orders/view_full_info_order/1",cookies=cookies)
    assert response.status_code == 404
    assert response.json()['detail'] == "Вашего активного заказа с таким id не найдено"

def test_bad_add_new_order_Nobacket():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/orders/add_new_order/?address=Филадельфия 2",cookies=cookies)
    assert response.status_code == 400
    assert response.json()['detail'] == "Вы не можете оформить заказ с пустой корзиной, или корзиной где только товары активных заказов."

def test_bad_delete_my_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.delete("/orders/delete_my_order/4",cookies=cookies)
    assert response.status_code == 404
    assert response.json()['detail'] == "Заказа с таким id не найдено"

def test_add_new_item_for_backet():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/backet/add_new_item_for_backet/1", cookies=cookies)

    assert response.status_code == 201
    assert response.json()['content'] == "Вы успешно добавили новый предмет в корзину"

    response2 = client.get("/backet/get_my_backet/", cookies=cookies)

    assert response2.status_code == 200
    assert response2.json() == [
  {
    "metainfo": {
      "backet_id": 2,
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

def test_add_new_order():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post("/orders/add_new_order/?address=Филадельфия 2",cookies=cookies)
    assert response.status_code == 201
    assert response.json()['content'] == "Добавление нового заказа произошло успешно!"

    response1 = client.get("/orders/view_my_active_order/", cookies=cookies)
    assert response1.status_code == 200
    assert response1.json() == {
  "active_order": [
    {
      "id": 1,
      "price_order": 100,
      "status": "Готовится",
      "address": "Филадельфия 2",
      "user_id": 1,
      "courier_id": None
    },
  ]
}

    response2 = client.get("/orders/view_full_info_order/1", cookies=cookies)
    assert response2.status_code == 200
    assert response2.json() == {
  "order_info": {
    "id": 1,
    "price_order": 100,
    "status": "Готовится",
    "address": "Филадельфия 2",
    "user_id": 1,
    "courier_id": None
  },
  "full_data_for_items": [
    {
      "metainfo": {
        "backet_id": 2,
        "user_id": 1,
        "item_id": 1,
        "order_id": 1
      },
      "item_info": [
        {
          "id": 1,
          "title": "Рыбка под соусом",
          "description": "Самая вкусная рыба в мире",
          "price": 100.0,
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




def test_logout():
    cookies = {'authenticate_user' : str(client.cookies.get('authenticate_user'))}
    response = client.post(url="/auth/logout", cookies=cookies)
    assert  response.status_code == 204
    assert not response.cookies

