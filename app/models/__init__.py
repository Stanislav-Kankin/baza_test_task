# Import models so Alembic can discover them via Base.metadata
from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.request import Request  # noqa: F401
