import uuid
from datetime import date

from sqlalchemy import ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserSchedule(Base):
  __tablename__ = 'user_schedules'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('user.id', ondelete='CASCADE')
  )
  name: Mapped[str | None] = mapped_column(String(100))
  created_at: Mapped[date] = mapped_column(server_default=func.now())
