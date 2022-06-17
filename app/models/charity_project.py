from sqlalchemy import Column, Integer, String, Text

from app.core.db import Base

from .abstract import Abstract


class CharityProject(Abstract, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, unique=True, nullable=False)
    full_amount = Column(Integer)
