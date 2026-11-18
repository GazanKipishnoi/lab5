from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={"email": "missing@example.org"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_valid_email():
    user = {"name": "Alexey", "email": "a.yu.assaulov@edu.mtuci.ru"}
    response = client.post("/api/v1/user", json=user)
    try:
        assert response.status_code == 201
        user_id = response.json()
        assert type(user_id) is int
        saved = client.get("/api/v1/user", params={"email": user["email"]})
        assert saved.json() == {"id": user_id, **user}
    finally:
        client.delete("/api/v1/user", params={"email": user["email"]})


def test_create_user_with_invalid_email():
    response = client.post("/api/v1/user", json={
        "name": "Another user", "email": users[0]["email"]
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"


def test_delete_user():
    user = {"name": "Test", "email": "delete@example.org"}
    assert client.post("/api/v1/user", json=user).status_code == 201
    params = {"email": user["email"]}
    response = client.delete("/api/v1/user", params=params)
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/api/v1/user", params=params).status_code == 404
