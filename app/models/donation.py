from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .abstract import Abstract


class Donation(Abstract, Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text, nullable=True)
