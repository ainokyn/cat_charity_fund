from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def delete(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """
        Удаляет проект, с проверкой наличия инвестиции в этом проекте.
        """
        if db_obj.invested_amount == 0:
            await session.delete(db_obj)
            await session.commit()
            return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """
        Обновляет проект,
        с проверкой что порект не закрыт и что новая сумма
        пожервования не меньше суммы инвестиций.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        if db_obj.fully_invested is not True and update_data['full_amount'] > obj_data['invested_amount']:
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """
        Получает id проекта по имени этого объекта.
        """
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = project_id.scalars().first()
        return db_project_id


charityproject_crud = CRUDCharityProject(CharityProject)
