import uuid

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CourseLab(Base):
  __tablename__ = 'course_labs'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  course_theory_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('course_theories.id', ondelete='CASCADE')
  )
