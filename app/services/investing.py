from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    donations = await session.execute(
        select(Donation).where(~Donation.fully_invested))
    donations = donations.scalars().all()
    projects = await session.execute(
        select(CharityProject).where(~CharityProject.fully_invested))
    projects = projects.scalars().all()
    donation_n = 0
    project_n = 0
    while donation_n < len(donations) and project_n < len(projects):
        free_for_investing = min(
            donations[donation_n].full_amount -
            donations[donation_n].invested_amount,
            projects[project_n].full_amount -
            projects[project_n].invested_amount)
        donations[donation_n].invested_amount += free_for_investing
        projects[project_n].invested_amount += free_for_investing
        if (donations[donation_n].full_amount ==
                donations[donation_n].invested_amount):
            setattr(donations[donation_n], 'fully_invested', True)
            setattr(donations[donation_n], 'close_date', datetime.now())
            donation_n += 1
        if (projects[project_n].full_amount ==
                projects[project_n].invested_amount):
            setattr(projects[project_n], 'fully_invested', True)
            setattr(projects[project_n], 'close_date', datetime.now())
            project_n += 1
    session.add_all(donations + projects)
    await session.commit()
