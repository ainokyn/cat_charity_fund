from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.sql import func


class Abstract():
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime, nullable=True)

    class Meta:
        abstract = True
