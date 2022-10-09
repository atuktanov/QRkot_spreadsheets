from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self, name: str, session: AsyncSession) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name))
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> list[dict]:
        projects = await session.execute(
            select(
                CharityProject.name, CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description).where(
                    CharityProject.fully_invested))
        result = []
        for obj in projects:
            result.append({
                'name': obj.name,
                'delta': obj.close_date - obj.create_date,
                'description': obj.description})
        return sorted(result, key=lambda x: x['delta'])


project_crud = CRUDCharityProject(CharityProject)
