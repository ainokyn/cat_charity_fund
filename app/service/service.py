from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invested(session: AsyncSession,):
    donat = await session.execute(
        select(Donation).where(Donation.fully_invested == False))# noqa
    donat = donat.scalars().all()
    project = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False).order_by(# noqa
                CharityProject.create_date.asc()))
    project = project.scalars().first()
    if project:
        project_sum = project.full_amount
        for item in donat:
            donat_sum = item.full_amount - item.invested_amount
            dict_item = {'fully_invested': True,
                         'close_date': datetime.now(),
                         'invested_amount': donat_sum
                         }
            dict_project = {'invested_amount': project_sum,
                            'fully_invested': True,
                            'close_date': datetime.now()
                            }
            if project_sum > donat_sum:
                if project.invested_amount != 0:
                    donat_sum += project.invested_amount
                else:
                    donat_sum = donat_sum
                setattr(project, 'invested_amount', donat_sum)
                for field in dict_item:
                    setattr(item, field, dict_item[field])
            if project_sum == donat_sum:
                for field in dict_item:
                    setattr(item, field, dict_item[field])
                for field in dict_project:
                    setattr(project, field, dict_project[field])
            if project_sum < donat_sum:
                if item.invested_amount != 0:
                    donat_sum = item.invested_amount - project_sum
                else:
                    delta = project_sum - project.invested_amount
                    donat_sum -= delta
                setattr(item, 'invested_amount', donat_sum)
                for field in dict_project:
                    setattr(project, field, dict_project[field])
            session.add(item)
            session.add(project)
            await session.commit()
            await session.refresh(item)
            await session.refresh(project)
            return item, project
