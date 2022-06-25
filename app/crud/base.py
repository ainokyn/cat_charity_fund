
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,

    ):
        """
        Получает объект по id.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
            self,
            session: AsyncSession
    ):
        """
        Получает список объектов.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
