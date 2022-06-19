from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def invested_donat(session: AsyncSession, db_obj):
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == False).order_by(# noqa
            CharityProject.create_date.asc()))
    project = project.scalars().first()
    if project:
        project_sum = project.full_amount - project.invested_amount
        full_amount_donat = db_obj.full_amount
        total = project.invested_amount + full_amount_donat
        dict_donat = {'fully_invested': True,
                      'close_date': datetime.now(),
                      'invested_amount': full_amount_donat
                      }
        if project_sum > full_amount_donat:
            for field in dict_donat:
                setattr(db_obj, field, dict_donat[field])
            setattr(project, 'invested_amount', total)
        if project_sum == full_amount_donat:
            for field in dict_donat:
                setattr(db_obj, field, dict_donat[field])
            setattr(project, 'invested_amount', total)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.now())
        if project_sum < full_amount_donat:
            delta = full_amount_donat - project_sum
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.now())
            setattr(db_obj, 'invested_amount', delta)
        session.add(db_obj)
        session.add(project)
        await session.commit()
        await session.refresh(db_obj)
        await session.refresh(project)
        return db_obj, project


async def upd(db_obj, obj_data, update_data):
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    return db_obj


async def val(db_obj, obj_data, update_data, session):
    if 'full_amount' in update_data:
        if update_data['full_amount'] < obj_data['invested_amount']:
            return None
        if update_data['full_amount'] > obj_data['invested_amount']:
            await upd(db_obj, obj_data, update_data)
        if update_data['full_amount'] == obj_data['invested_amount']:
            await upd(db_obj, obj_data, update_data)
            setattr(db_obj, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.now())
    if 'full_amount' not in update_data:
        await upd(db_obj, obj_data, update_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
