import uuid

from pydantic_extra_types import Color
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.types import ColorType


class Course(Base):
  __tablename__ = 'courses'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  study_plan_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('study_plans.id', ondelete='CASCADE')
  )
  code: Mapped[str] = mapped_column(String(7))
  name: Mapped[str] = mapped_column(String(150))
  recommended_year: Mapped[int]
  cycle: Mapped[str] = mapped_column(String(1))
  credits: Mapped[int]
  color: Mapped[Color] = mapped_column(ColorType())
