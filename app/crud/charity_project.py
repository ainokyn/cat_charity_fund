from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.service.service import invested_project, val


class CRUDCharityProject(CRUDBase):

    async def delete(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """
        Удаляет проект.
        """
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
        await val(db_obj, obj_data, update_data, session)
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

    async def create_project(
            self,
            obj_in,
            session: AsyncSession,
    ):
        """
        Создает объект проекта.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        await invested_project(session, db_obj)
        return db_obj


charityproject_crud = CRUDCharityProject(CharityProject)
