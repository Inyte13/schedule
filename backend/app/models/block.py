from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Block(Base):
  __tablename__ = 'blocks'
  number: Mapped[int] = mapped_column(primary_key=True)
  start_time: Mapped[str] = mapped_column(String(5))
  end_time: Mapped[str] = mapped_column(String(5))
