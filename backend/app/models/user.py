import uuid
from datetime import date, datetime

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
  __tablename__ = 'users'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid, primary_key=True, default=uuid.uuid4
  )
  google_id: Mapped[str] = mapped_column(unique=True, index=True)
  email: Mapped[str] = mapped_column(unique=True, index=True)
  email_verified: Mapped[bool]
  given_name: Mapped[str | None]
  family_name: Mapped[str | None]
  picture_url: Mapped[str | None]
  is_active: Mapped[bool] = mapped_column(default=True)
  created_at: Mapped[date] = mapped_column(server_default=func.now())
  deactivated_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), default=None
  )
