import uuid

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ScheduleSection(Base):
  __tablename__ = 'schedules_sections'
  __table_args__ = (PrimaryKeyConstraint('user_schedule_id', 'section_id'),)
  user_schedule_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('user_schedules.id', ondelete='CASCADE')
  )
  section_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey('sections.id', ondelete='CASCADE')
  )
