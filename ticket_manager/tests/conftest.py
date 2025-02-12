import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ticket_manager.app import app
from ticket_manager.database import get_session
from ticket_manager.models import Manager, mapper_registry
from ticket_manager.security import hash_password


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session):
    """Cria um usuário de teste no banco de dados."""
    user = Manager(username="testuser", password=hash_password("testpassword"))
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def access_token(client, test_user):
    """Gera um token de acesso para o usuário de teste."""
    response = client.post(
        "/auth/token",
        data={"username": test_user.username, "password": "testpassword"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(access_token):
    """Retorna os cabeçalhos de autenticação para testes protegidos."""
    return {"Authorization": f"Bearer {access_token}"}
