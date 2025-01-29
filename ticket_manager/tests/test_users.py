from http import HTTPStatus


def test_hello(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/",
        json={"username": "alice", "password": "secret"},
    )
    print(response.json())  # Debugging output
    assert response.status_code == HTTPStatus.CREATED
