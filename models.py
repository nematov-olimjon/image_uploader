from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


# Define To Do class inheriting from Base
class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer)
    name = Column(String(256), primary_key=True)
    image_size = Column(Integer)
    file_extension = Column(String(7))
    updated_at = Column(String(100))
