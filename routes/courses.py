from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.courses import create_course, course_images, update_course, delete_course, get_all_course, get_all_group, create_group, update_group, delete_group, update_group_status
from models.courses import Courses, Groups
from routes.auth import get_current_active_user
from schemas.courses import CreateGroup, UpdateGroup
from schemas.users import CreateUser
from sqlalchemy.future import select

course_router = APIRouter(
    prefix="/course",
    tags=["Course operation"]
)


group_router = APIRouter(
    prefix="/group",
    tags=["Group operation"]
)


@course_router.get('/get')
async def barcha_kurslar(db: AsyncSession = Depends(get_database),
                         current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_course(db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@course_router.get('/get_count')
async def kurslar_soni(db: AsyncSession = Depends(get_database),
                       current_user: CreateUser = Depends(get_current_active_user)):

    try:
        if current_user.role not in ['admin', 'boss']:
            raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

        result = await db.execute(select(Courses))
        course_count = len(result.scalars().all())
        return {"count": course_count}

    except Exception as e:
        raise HTTPException(400, str(e))


@course_router.post('/create')
async def kurs_qoshish(course_name: str, db: AsyncSession = Depends(get_database),
                       current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_course(course_name, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@course_router.post('/upload-image')
async def kursga_rasm_yuklash(ident:int, file: UploadFile = File(...), db: AsyncSession = Depends(get_database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await course_images(ident,file, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@course_router.put('/update')
async def kurs_tahrirlash(ident:int, new_name: str, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await update_course(ident, new_name, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@course_router.delete('/delete')
async def kurs_ochirish(ident:int, db: AsyncSession = Depends(get_database),
                        current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_course(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))



@group_router.get('/get')
async def barcha_guruhlar(course_id: int = None,db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_group(course_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@group_router.get('/get_count')
async def guruhlar_soni(db: AsyncSession = Depends(get_database),
                       current_user: CreateUser = Depends(get_current_active_user)):

    try:

        if current_user.role not in ['admin', 'boss']:
            raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

        result = await db.execute(select(Groups))
        course_count = len(result.scalars().all())
        return {"count": course_count}

    except Exception as e:
        raise HTTPException(400, str(e))


@group_router.post('/create')
async def guruh_qoshish(form: CreateGroup, db: AsyncSession = Depends(get_database),
                       current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_group(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@group_router.put('/update_status')
async def guruh_statusini_tahrirlash(ident:int, db: AsyncSession = Depends(get_database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_group_status(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@group_router.put('/update')
async def guruh_tahrirlash(ident:int, form: UpdateGroup, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await update_group(ident, form, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))


@group_router.delete('/delete')
async def guruh_ochirish(ident:int, db: AsyncSession = Depends(get_database),
                        current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_group(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, str(e))