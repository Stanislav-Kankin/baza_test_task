from fastapi import Request as FastAPIRequest
from sqlalchemy.orm import Session

from app.models.user import User


COOKIE_USER_ID = "user_id"


def get_current_user(db: Session, request: FastAPIRequest) -> User | None:
    """Very simple auth: user_id is stored in cookie.
    Returns User or None if not authenticated/invalid.
    """
    raw = request.cookies.get(COOKIE_USER_ID)
    if not raw:
        return None

    try:
        user_id = int(raw)
    except ValueError:
        return None

    return db.get(User, user_id)
