from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str]

    @validator('full_amount')
    def full_amount_not_zero(cls, value: int):
        if value < 0:
            raise ValueError('Cумма пожертвования должна быть больше 0!')
        return value


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
