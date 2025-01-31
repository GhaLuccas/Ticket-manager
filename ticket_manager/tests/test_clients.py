from http import HTTPStatus


def test_create_client(client):
    response = client.post(
        "/clients",
        json={"name": "alice",
            "company_name": "MyCompany",
            "phone": '1998281283',
            },
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
