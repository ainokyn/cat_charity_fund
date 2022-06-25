from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validator import (cant_delete, check_project_before_edit,
                               name_uniq, projects_is_exist)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.get('/', response_model=List[CharityProjectDB],
            response_model_exclude_none=True,)
async def get_all_charity(
        session: AsyncSession = Depends(get_async_session),):
    """
    Получает список всех проектов. Для всех пользователей.
    """
    await projects_is_exist(session)
    all_charity = await charityproject_crud.get_all(session)
    return all_charity


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)],
             response_model_exclude_none=True,)
async def create_charity(
        charity: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),):
    """
    Только для суперюзеров. Создает благотворительный проект.
    """
    await name_uniq(charity.name, session)
    charity = await charityproject_crud.create_project(charity, session)
    return charity


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)],)
async def delete_charity(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),):
    """
    Только для суперюзеров.Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    charity = await cant_delete(project_id, session)
    charity = await charityproject_crud.delete(charity, session)
    return charity


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],)
async def patch_charity(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),):
    """
    Только для суперюзеров.Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    if obj_in.name is not None:
        await name_uniq(obj_in.name, session)
    charity = await check_project_before_edit(project_id, session)
    charity = await charityproject_crud.update(charity, obj_in, session)
    return charity
