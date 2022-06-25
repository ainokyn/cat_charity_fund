from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validator import donate_is_exist, donats_is_exist
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDB_Full

router = APIRouter()


@router.get('/',
            response_model=List[DonationDB_Full],
            dependencies=[Depends(current_superuser)],
            response_model_exclude_none=True,
            )
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),):
    """
    Только для суперюзеров.Получает список всех пожертвований.
    """
    await donats_is_exist(session)
    all_donation = await donation_crud.get_all(session)
    return all_donation


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True,
             )
async def create_donations(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),):
    """
    Сделать пожертвование. Только для зарегистрированных.
    """
    donation = await donation_crud.create_donat(donation, session, user)
    return donation


@router.get('/my', response_model=List[DonationDB],
            )
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),):
    """
    Получить список своих пожертвований. Только для зарегистрированных.
    """
    await donate_is_exist(user, session)
    donation = await donation_crud.my_donations(user, session)
    return donation
