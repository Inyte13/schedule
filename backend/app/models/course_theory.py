import uuid

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CourseTheory(Base):
  __tablename__ = 'course_theories'
  id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    default=uuid.uuid4,
  )
  course_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('courses.id', ondelete='CASCADE')
  )
  
