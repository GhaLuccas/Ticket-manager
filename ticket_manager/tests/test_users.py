from http import HTTPStatus

from ticket_manager.models import Manager


def test_create_user_with_existing_username(client, session):
    """Testa a criação de um usuário com um nome já existente."""
    user1 = Manager(username="alice123", password="password123")
    session.add(user1)
    session.commit()

    payload = {"username": "alice123", "password": "newpassword"}
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "User already exist"


def test_create_user_success(client):
    """Testa a criação bem-sucedida de um usuário."""
    payload = {"username": "bob456", "password": "password456"}
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["username"] == payload["username"]


def test_create_user_missing_field(client):
    """Testa a criação de usuário com campos faltando."""
    payload = {"username": "bob456"}
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_users(client, session, auth_headers):
    """Testa a listagem de usuários."""
    session.add_all([
        Manager(username="alice123", password="password123"),
        Manager(username="bob456", password="password456")
    ])
    session.commit()

    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    two = 2
    assert len(data["userlist"]) >= two
    assert any(user["username"] == "alice123" for user in data["userlist"])
    assert any(user["username"] == "bob456" for user in data["userlist"])


def test_get_user(client, session, auth_headers):
    """Testa a recuperação de um usuário específico."""
    new_user = Manager(username="charlie789", password="password789")
    session.add(new_user)
    session.commit()

    response = client.get(f"/users/{new_user.id}", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == new_user.username


def test_get_user_not_found(client, auth_headers):
    """Testa a busca por um usuário inexistente."""
    response = client.get("/users/999", headers=auth_headers)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_success(client, session, test_user, auth_headers):
    response = client.delete(
        f"/users/{test_user.id}",
        headers=auth_headers
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
