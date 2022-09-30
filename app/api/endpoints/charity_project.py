from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate,
                                check_project_before_delete,
                                check_project_before_edit)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/', response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    '''Только для суперюзеров.\n
    Создаёт благотворительный проект.'''
    await check_name_duplicate(project.name, session)
    project = await project_crud.create(project, session)
    await investing(session)
    await session.refresh(project)
    return project


@router.get(
    '/', response_model=list[CharityProjectDB],
    response_model_exclude_none=True)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    '''Возвращает список всех проектов.'''
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}', response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def partially_update_project(
        project_id: int, obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)):
    '''Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
     нельзя установить требуемую сумму меньше уже вложенной.'''
    project = await check_project_before_edit(project_id, obj_in, session)
    await check_name_duplicate(obj_in.name, session)
    await project_crud.update(project, obj_in, session)
    await investing(session)
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}', response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def remove_project(
        project_id: int, session: AsyncSession = Depends(get_async_session)):
    '''Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект,
     в который уже были инвестированы средства, его можно только закрыть.'''
    project = await check_project_before_delete(project_id, session)
    return await project_crud.remove(project, session)
