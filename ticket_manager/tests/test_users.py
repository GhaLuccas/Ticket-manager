from http import HTTPStatus

from ticket_manager.models import Manager


def test_create_user_with_existing_username(client, session):

    user1 = Manager(username="alice123", password="password123")
    session.add(user1)
    session.commit()

    payload = {
        "username": "alice123",
        "password": "newpassword"
    }
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Username already taken"


def test_create_user_success(client, session):

    payload = {
        "username": "bob456",
        "password": "password456"
    }
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["password"] == payload["password"]


def test_create_user_missing_field(client):
    payload = {
        "username": "bob456"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_users(client, session):
    session.add_all([
        Manager(username="alice123", password="password123"),
        Manager(username="bob456", password="password456")
    ])
    session.commit()

    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    len_should_be = 2
    assert len(data) == len_should_be
    assert data[0]["username"] == "alice123"
    assert data[1]["username"] == "bob456"


def test_get_user(client, session):
    new_user = Manager(username="charlie789", password="password789")
    session.add(new_user)
    session.commit()

    response = client.get(f"/users/{new_user.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["username"] == new_user.username


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, session):
    user_to_delete = Manager(username="deleteMe", password="deletePassword")
    session.add(user_to_delete)
    session.commit()

    response = client.delete(f"/users/{user_to_delete.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert session.get(Manager, user_to_delete.id) is None


def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
