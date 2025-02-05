from http import HTTPStatus

from ticket_manager.models import Client


def test_create_client(client):
    payload = {
        "name": "Alice",
        "company_name": "TechCorp",
        "phone": "123456789"
        }
    response = client.post("/clients/", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["company_name"] == payload["company_name"]
    assert data["phone"] == payload["phone"]


def test_create_client_defaults(client):
    payload = {"name": "Maria"}
    response = client.post("/clients/", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["company_name"] == "Não cadastrado"
    assert data["phone"] == "Não cadastrado"


def test_update_client(client, session):
    new_client = Client(
        name="Carlos", company_name="OldCorp", phone="987654321"
        )
    session.add(new_client)
    session.commit()

    payload = {"name": "Carlos Novo", "company_name": "NewCorp"}
    response = client.put(f"/clients/{new_client.id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Carlos Novo"
    assert data["company_name"] == "NewCorp"
    assert data["phone"] == "987654321"


def test_update_client_not_found(client):
    response = client.put("/clients/999", json={"name": "Not Exists"})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_search_clients(client, session):
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=''),
        Client(name="Bob", company_name="BetaTech", phone=''),
    ])
    session.commit()

    response = client.get("/clients/?search_term=Alpha")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data['clientlist'][0]["company_name"] == "AlphaTech"


def test_search_clients_all(client, session):
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=''),
        Client(name="Bob", company_name="BetaTech", phone=''),
        Client(name="GothGirl", company_name="DadIssue", phone='666'),
    ])
    session.commit()

    response = client.get("/clients/?search_term=")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    len_should_be = 3
    assert len(data['clientlist']) == len_should_be
    assert data['clientlist'][2]["name"] == "GothGirl"


def test_search_clients_notfound(client, session):
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=''),
        Client(name="Bob", company_name="BetaTech", phone=''),
    ])
    session.commit()

    response = client.get("/clients/?search_term=gothgirl")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_client(client, session):
    client_to_delete = Client(
        name="DeleteMe",
        company_name="TestCorp",
        phone=''
        )
    session.add(client_to_delete)
    session.commit()

    response = client.delete(f"/clients/{client_to_delete.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert session.get(Client, client_to_delete.id) is None


def test_delete_client_not_found(client):
    response = client.delete("/clients/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
