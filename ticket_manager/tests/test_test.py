from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/create',
        json={
            'username': 'alice',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'password': 'secret',
        'id': 1,
    }
