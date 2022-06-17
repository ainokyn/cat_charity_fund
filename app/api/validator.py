from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation, User


async def name_uniq(project_name: str,
                    session: AsyncSession) -> None:
    """
    Проверяет уникальность имени проекта.
    """
    project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session)
    if project_id:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def project_is_exist(id: int,
                           session: AsyncSession) -> CharityProject:
    """
    Проверяет существование проекта.
    """
    project = await charityproject_crud.get(id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта нет!',
        )
    return project


async def projects_is_exist(session: AsyncSession) -> list[CharityProject]:
    """
    Проверяет существование проектов.
    """
    projects = await charityproject_crud.get_all(session)
    if not projects:
        raise HTTPException(
            status_code=404,
            detail='Проектов еще нет!',
        )
    return projects


async def donate_is_exist(user: User,
                          session: AsyncSession
                          ) -> list[Donation]:
    """
    Проверяет существование доната.
    """
    donates = await donation_crud.my_donations(user, session)
    if not donates:
        raise HTTPException(
            status_code=404,
            detail='Ты еще не задонатил!',
        )
    return donates


async def donats_is_exist(session: AsyncSession) -> list[Donation]:
    """
    Проверяет существование донатов.
    """
    donates = await donation_crud.get_all(session)
    if not donates:
        raise HTTPException(
            status_code=404,
            detail='Донатов еще нет!',
        )
    return donates


async def cant_delete(*kwargs) -> None:
    """
    Проверяет можно ли удалить проект.
    """
    db_obj = await charityproject_crud.delete(*kwargs)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def cant_update(*kwargs) -> None:
    """
    Проверяет можно ли обновить частично проект.
    """
    db_obj = await charityproject_crud.update(*kwargs)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )
