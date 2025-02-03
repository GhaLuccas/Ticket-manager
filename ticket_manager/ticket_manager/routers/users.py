from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Manager
from ticket_manager.schema import (
    UserListPublicShema,
    UserManagerSchema,
    UserPublicSchema,
)

SessionDep = Annotated[Session, Depends(get_session)]

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post(
    '/',
    status_code=201,
    response_model=UserPublicSchema
    )
def create_user(user: UserManagerSchema, session: SessionDep):
    existing_user = session.query(Manager).filter(
        Manager.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    try:
        user_manager = Manager(
            username=user.username,
            password=user.password,
        )
        session.add(user_manager)
        session.commit()
        session.refresh(user_manager)
        return {'id': user_manager.id, 'username': user_manager.username}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Username already taken")


@users_router.get(
    '/',
    response_model=UserListPublicShema,
    status_code=200)
def get_users(session: SessionDep):
    users = session.query(Manager).all()
    return {
        'userlist': [
            {'id': user.id, 'username': user.username} for user in users]}


@users_router.get(
    '/{user_id}',
    response_model=UserPublicSchema,
    status_code=200)
def get_user(user_id: int, session: SessionDep):
    user = session.query(Manager).filter(Manager.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {'username': user.username, 'id': user.id}


@users_router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, session: SessionDep):
    user = session.query(Manager).filter(Manager.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
