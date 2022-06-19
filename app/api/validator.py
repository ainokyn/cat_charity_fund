from typing import List

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


async def projects_is_exist(session: AsyncSession) -> List[CharityProject]:
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
                          ) -> List[Donation]:
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


async def donats_is_exist(session: AsyncSession) -> List[Donation]:
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


async def cant_delete(project_id: int,
                      session: AsyncSession,) -> CharityProject:
    """
    Проверяет можно ли удалить проект.
    """
    project = await charityproject_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession,

) -> CharityProject:
    """
    Проверяет можно ли обновить частично проект.
    """
    project = await charityproject_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )
    return project
