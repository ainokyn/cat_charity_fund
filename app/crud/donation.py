from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation
from app.service.service import invested_donat


class CRUDDonationProject(CRUDBase):

    async def my_donations(self,
                           user: User,
                           session: AsyncSession,) -> List[Donation]:
        """
        Получает список донатов определенного пользователя.
        """
        donation = await session.execute(select(Donation).where(Donation.user_id == user.id))
        donation = donation.scalars().all()
        return donation

    async def create_donat(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        """
        Создает объект доната.
        """
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await invested_donat(session, db_obj)
        return db_obj


donation_crud = CRUDDonationProject(Donation)
