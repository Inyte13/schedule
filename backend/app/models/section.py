import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Section(Base):
  __tablename__ = 'sections'
  # Para que solo 1 de los id's sea obligatorio y el otro nullable
  __table_args__ = (
    CheckConstraint(
      'num_nonnulls(course_theory_id, course_lab_id) = 1',
      name='ck_sections_exactly_one_course_component',
    ),
  )
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  course_theory_id: Mapped[uuid.UUID | None] = mapped_column(
    ForeignKey('course_theories.id', ondelete='CASCADE')
  )
  course_lab_id: Mapped[uuid.UUID | None] = mapped_column(
    ForeignKey('course_labs.id', ondelete='CASCADE')
  )
  label: Mapped[str] = mapped_column(String(1))
  professor_name: Mapped[str] = mapped_column(String(150))
  schedule: Mapped[str] = mapped_column(String(255))  
