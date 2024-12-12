from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Word(Base):
    __tablename__ = "word"
    english: Mapped[str] = mapped_column(String(128))
    russian: Mapped[Optional[str]] = mapped_column(String(128), default=None)
    transcription: Mapped[Optional[str]] = mapped_column(String(128), default=None)
    link: Mapped[Optional[str]] = mapped_column(String(256), default=None)


