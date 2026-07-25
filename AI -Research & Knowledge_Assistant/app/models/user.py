from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )