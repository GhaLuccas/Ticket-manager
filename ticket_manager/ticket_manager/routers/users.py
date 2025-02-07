
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from ticket_manager.database import session_db
from ticket_manager.models import Manager
from ticket_manager.schema import (
    UserListPublicShema,
    UserManagerSchema,
    UserPublicSchema,
)
from ticket_manager.services.users_services import get_user_by_id, user_exist

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post(
    '/',
    status_code=201,
    response_model=UserPublicSchema
    )
def create_user(user: UserManagerSchema, session: session_db):

    new_user = user_exist(session, user)

    try:
        new_user = Manager(
            username=new_user.username,
            password=new_user.password,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {'id': new_user.id, 'username': new_user.username}
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already taken")


@users_router.get(
    '/',
    response_model=UserListPublicShema,
    status_code=200)
def get_users(session: session_db):
    users = session.query(Manager).all()
    return {
        'userlist': [
            {'id': user.id, 'username': user.username} for user in users]}


@users_router.get(
    '/{user_id}',
    response_model=UserPublicSchema,
    status_code=200)
def get_user(user_id: int, session: session_db):
    user = get_user_by_id(session, user_id)
    return {'username': user.username, 'id': user.id}


@users_router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, session: session_db):
    user = get_user_by_id(session, user_id)
    session.delete(user)
    session.commit()
