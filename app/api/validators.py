from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str, session: AsyncSession) -> None:
    project_id = await project_crud.get_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!')


async def check_project_exists(
        project_id: int, session: AsyncSession) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!')
    return project


async def check_project_before_edit(
        project_id: int, obj_in: CharityProjectUpdate,
        session: AsyncSession) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if obj_in.full_amount and project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!')
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!')
    return project


async def check_project_before_delete(
        project_id: int, session: AsyncSession) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!')
    return project
