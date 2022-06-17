from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProject(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int

    @validator('full_amount')
    def full_amount_not_zero(cls, value: int):
        if value < 0:
            raise ValueError('Cумма пожертвования должна быть больше 0!')
        return value

    @validator('name')
    def name_len(cls, value: int):
        if len(value) > 100:
            raise ValueError('Слишком длинное имя проекта!')
        return value

    @validator('description')
    def description_len(cls, value: int):
        if len(value) < 1:
            raise ValueError('Слишком короткое описание проекта!')
        return value


class CharityProjectCreate(CharityProject):
    pass


class CharityProjectDB(CharityProject):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProject):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: Optional[int]
