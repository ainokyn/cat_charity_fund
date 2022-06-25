from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invested_project(session: AsyncSession, db_obj):
    """
    Функция для расчета инвестиций для проекта.
    """
    donat = await session.execute(select(Donation))
    donat = donat.scalars().first()
    if donat:
        project_sum, full_amount_donat, total, dict_donat, invested_amount = await advanced(db_obj, donat)
        if project_sum > full_amount_donat:
            await project_summ_more_than_donat(dict_donat, donat, db_obj, total, full_amount_donat)
        if project_sum == full_amount_donat:
            await project_summ_equal_to_donat(dict_donat, donat, db_obj, total, invested_amount)
        if project_sum < full_amount_donat:
            full_amount = db_obj.full_amount
            await project_summ_less_than_donat(donat, db_obj, invested_amount, full_amount)
        session.add(donat)
        session.add(db_obj)
        await session.commit()
        await session.refresh(donat)
        await session.refresh(db_obj)
        return db_obj


async def invested_donat(session: AsyncSession, db_obj):
    """
    Функция для расчета инвестиций для доната.
    """
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == False).order_by(# noqa
            CharityProject.create_date.asc()))
    project = project.scalars().first()
    if project:
        project_sum, full_amount_donat, total, dict_donat, invested_amount = await advanced(project, db_obj)
        if project_sum > full_amount_donat:
            await project_summ_more_than_donat(dict_donat, db_obj, project, total, full_amount_donat)
        if project_sum == full_amount_donat:
            await project_summ_equal_to_donat(dict_donat, db_obj, project, total, invested_amount)
        if project_sum < full_amount_donat:
            full_amount = project.full_amount
            await project_summ_less_than_donat(db_obj, project, invested_amount, full_amount)
        session.add(db_obj)
        session.add(project)
        await session.commit()
        await session.refresh(db_obj)
        await session.refresh(project)
        return db_obj


async def advanced(project, donat):
    """
    Вспомогательная функция для расчета project_sum,
    full_amount_donat, total и передачи словаря dict_donat.
    """
    project_sum = project.full_amount - project.invested_amount
    full_amount_donat = donat.full_amount - donat.invested_amount
    total = project.invested_amount + full_amount_donat
    invested_amount = project.full_amount + donat.invested_amount
    dict_donat = {'fully_invested': True,
                  'close_date': datetime.now()
                  }
    return project_sum, full_amount_donat, total, dict_donat, invested_amount


async def project_summ_more_than_donat(dict_donat, donat, project, total, full_amount_donat):
    """
    Вспомогательная функция для обработки варианта,
    где сумма проекта больше суммы доната.
    """
    for field in dict_donat:
        setattr(donat, field, dict_donat[field])
    setattr(donat, 'invested_amount', full_amount_donat)
    setattr(project, 'invested_amount', total)
    return project, donat


async def project_summ_equal_to_donat(dict_donat, donat, project, total, invested_amount):
    """
    Вспомогательная функция для обработки варианта,
    где сумма проекта равна сумме доната.
    """
    for field in dict_donat:
        setattr(donat, field, dict_donat[field])
    setattr(donat, 'invested_amount', invested_amount)
    setattr(project, 'invested_amount', total)
    setattr(project, 'fully_invested', True)
    setattr(project, 'close_date', datetime.now())
    return project, donat


async def project_summ_less_than_donat(donat, project, invested_amount, full_amount):
    """
    Вспомогательная функция для обработки варианта,
    где сумма проекта меньше суммы доната.
    """
    setattr(project, 'invested_amount', full_amount)
    setattr(project, 'fully_invested', True)
    setattr(project, 'close_date', datetime.now())
    setattr(donat, 'invested_amount', invested_amount)
    return project, donat


async def upd(db_obj, obj_data, update_data):
    """
    Вспомогательная функция для обновления полей модели.
    """
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    return db_obj


async def val(db_obj, obj_data, update_data, session):
    """
    Функция для перерасчета инвестиций при обновлении проекта.
    """
    if 'full_amount' in update_data:
        if update_data['full_amount'] < obj_data['invested_amount']:
            return None
        if update_data['full_amount'] > obj_data['invested_amount']:
            await upd(db_obj, obj_data, update_data)
        if update_data['full_amount'] == obj_data['invested_amount']:
            setattr(db_obj, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.now())
            await upd(db_obj, obj_data, update_data)
    if 'full_amount' not in update_data:
        await upd(db_obj, obj_data, update_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
