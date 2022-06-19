from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, root_validator


class CharityProject(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProject):

    @validator('name')
    def name_len(cls, value: str):
        if len(value) > 100:
            raise ValueError('Слишком длинное имя проекта!')
        return value

    @validator('description')
    def description_len(cls, value: str):
        if len(value) < 1:
            raise ValueError('Слишком короткое описание проекта!')
        return value

    @root_validator(skip_on_failure=True)
    def field_validator(cls, values):
        if values['description'] is None:
            raise ValueError(
                'Поле описание не должно быть пустым'
            )
        if values['name'] is None:
            raise ValueError(
                'Поле имя не должно быть пустым'
            )
        if values['full_amount'] is None:
            raise ValueError(
                'Поле проект не должно быть пустым'
            )
        return values


class CharityProjectUpdate(CharityProjectCreate):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: Optional[int]


class CharityProjectDB(CharityProjectUpdate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True