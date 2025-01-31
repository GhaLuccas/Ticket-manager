from http import HTTPStatus


def test_hello(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "alice", "password": "secret"},
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
