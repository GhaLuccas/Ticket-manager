from fastapi import HTTPException

from ticket_manager.database import session_db
from ticket_manager.models import Manager
from ticket_manager.schema import UserManagerSchema


def ensure_user_exist_or_400(db: session_db, user: UserManagerSchema):
    exist_user = db.query(Manager).filter(
        Manager.username == user.username
        ).first()
    if not exist_user:
        return user
    else:
        raise HTTPException(
            status_code=400,
            detail="User already exist"
            )


def get_user_by_id_or_404(db: session_db, user_id: int):
    user = db.query(Manager).filter(Manager.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
