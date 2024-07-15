import pytest
from .conftest import client, async_session_maker
from sqlalchemy import insert, select, update
from auth.models import user

async def test_add_super_user():
    async with async_session_maker() as session:
        query = update(user).values(is_superuser=True).where(user.c.email == "restor@example.com")
        await session.execute(query)
        await session.commit()
        
        query1 = select(user).where(user.c.email == "restor@example.com")
        result = session.execute(query1)
        return result

def test_login_rest():
    response = client.post(url="/auth/login", data={"username" : "restor@example.com", "password" : 'string'})
    assert response.status_code == 204
    assert response.cookies.keys

