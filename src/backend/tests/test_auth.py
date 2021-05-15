from aiohttp.test_utils import TestClient as _TestClient


async def test_signup_view(database, client: _TestClient):
    valid_form = {
        'login': 'Joe',
        'password': '123',
        'confirmed_password': '123'
    }
    resp = await client.post('/signup', data=valid_form)
    assert resp.status == 200
    invalid_form = {
        'login': 'Sam',
        'password': '123',
        'confirmed_password': '1234'
    }
    resp = await client.post('/signup', data=invalid_form)
    assert {'status': 'error', 'reason': 'Bad Request'} == await resp.json()
    assert resp.status == 400

    # todo process repeating error
    resp = await client.post('/signup', data=valid_form)
    assert resp.status == 500
    resp = await resp.json()
    assert resp["status"] == "failed"


async def test_login(database, client: _TestClient):
    valid_form = {
        'login': 'Adam',
        'password': 'adam',
        'confirmed_password': 'adam'
    }
    resp = await client.post('/signup', data=valid_form)
    assert resp.status == 200
    del valid_form["confirmed_password"]
    resp = await client.post('/login', data=valid_form)
    assert resp.status == 200
    invalid_form = {
        'login': 'Adam',
        'password': 'adam_Wrong'
    }
    resp = await client.post('/login', data=invalid_form)
    assert resp.status == 401


async def test_logout(database, client: _TestClient):
    valid_form = {
        'login': 'Adam',
        'password': 'adam',
        'confirmed_password': 'adam'
    }
    resp = await client.post('/signup', data=valid_form)
    assert resp.status == 200
    del valid_form["confirmed_password"]
    resp = await client.post('/login', data=valid_form)
    assert resp.status == 200
    resp = await client.get('/logout')
    assert resp.status == 200
