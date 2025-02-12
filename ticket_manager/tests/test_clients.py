from http import HTTPStatus

from ticket_manager.models import Client


def test_create_client(client, auth_headers):
    """Testa a criação de um cliente autenticado."""
    payload = {
        "name": "Alice",
        "company_name": "TechCorp",
        "phone": "123456789"
    }
    response = client.post("/clients/", json=payload, headers=auth_headers)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["company_name"] == payload["company_name"]
    assert data["phone"] == payload["phone"]


def test_create_client_defaults(client, auth_headers):
    """Testa a criação de um cliente sem todos os campos (valores padrão)."""
    payload = {"name": "Maria"}
    response = client.post(
        "/clients/", json=payload, headers=auth_headers
        )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["company_name"] == "Não cadastrado"
    assert data["phone"] == "Não cadastrado"


def test_update_client(client, session, auth_headers):
    """Testa a atualização de um cliente existente."""
    existing_client = Client(
        name="Carlos", company_name="OldCorp", phone="987654321"
        )
    session.add(existing_client)
    session.commit()

    payload = {"name": "Carlos Novo", "company_name": "NewCorp"}
    response = client.put(
        f"/clients/{existing_client.id}", json=payload, headers=auth_headers
        )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Carlos Novo"
    assert data["company_name"] == "NewCorp"
    assert data["phone"] == "987654321"  # O campo phone não foi atualizado


def test_update_client_not_found(client, auth_headers):
    """Testa a tentativa de atualizar um cliente inexistente."""
    response = client.put(
        "/clients/999", json={"name": "Not Exists"}, headers=auth_headers
        )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_search_clients(client, session, auth_headers):
    """Testa a busca por clientes com um termo específico."""
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=""),
        Client(name="Bob", company_name="BetaTech", phone=""),
    ])
    session.commit()

    response = client.get(
        "/clients/?search_term=Alpha", headers=auth_headers
        )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data["clientlist"]) == 1
    assert data["clientlist"][0]["company_name"] == "AlphaTech"


def test_search_clients_all(client, session, auth_headers):
    """busca sem um termo específico (deve retornar todos os clientes)."""
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=""),
        Client(name="Bob", company_name="BetaTech", phone=""),
        Client(name="GothGirl", company_name="DadIssue", phone="666"),
    ])
    session.commit()

    response = client.get("/clients/?search_term=", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    one = 3
    assert len(data["clientlist"]) == one
    assert data["clientlist"][2]["name"] == "GothGirl"


def test_search_clients_not_found(client, session, auth_headers):
    """busca por um termo que não corresponde a nenhum nada."""
    session.add_all([
        Client(name="Alice", company_name="AlphaTech", phone=""),
        Client(name="Bob", company_name="BetaTech", phone=""),
    ])
    session.commit()

    response = client.get(
        "/clients/?search_term=gothgirl", headers=auth_headers
        )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_client(client, session, auth_headers):
    """Testa a exclusão de um cliente existente."""
    client_to_delete = Client(
        name="DeleteMe", company_name="TestCorp", phone=""
        )
    session.add(client_to_delete)
    session.commit()

    response = client.delete(
        f"/clients/{client_to_delete.id}", headers=auth_headers
        )
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert session.get(Client, client_to_delete.id) is None


def test_delete_client_not_found(client, auth_headers):
    """Testa a tentativa de deletar um cliente que não existe."""
    response = client.delete("/clients/999", headers=auth_headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
