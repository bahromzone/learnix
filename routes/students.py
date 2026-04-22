from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.students import get_own_student, create_student, update_student, delete_student, get_all_students, update_status, get_debtors_by_year_month
from sqlalchemy.future import select
from models.students import Students
from routes.auth import get_current_active_user
from schemas.students import CreateStudent, UpdateStudent, UpdateStatus
from schemas.users import CreateUser


student_router = APIRouter(
    prefix="/student",
    tags=["Student operation"]
)


@student_router.get('/get_all_students')
async def barcha_oquvchilarni_korish(group_id: int = None, status: str = None, db: AsyncSession = Depends(get_database),
                                     current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_students(group_id, status, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.get('/get_debt_student')
async def qarzdor_oquvchilarni_korish(year:int = None, month:str = None, db: AsyncSession = Depends(get_database),
                                     current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_debtors_by_year_month(year,month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.get('/get_own_students')
async def oquvchilarni_korish(group_id: int = None,db: AsyncSession = Depends(get_database),
                        current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_own_student(group_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.get('/get_count')
async def oquvchilar_soni(db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):

    try:
        if current_user.role not in ['admin', 'boss']:
            raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

        active_result = await db.execute(select(Students).where(Students.status == 'active'))
        active_student_count = len(active_result.scalars().all())

        inactive_result = await db.execute(select(Students).where(Students.status == 'inactive'))
        inactive_student_count = len(inactive_result.scalars().all())

        graduated_result = await db.execute(select(Students).where(Students.status == 'graduated'))
        graduated_student_count = len(graduated_result.scalars().all())


        return {
            "active_count": active_student_count,
            "inactive_count": inactive_student_count,
            "graduated_count": graduated_student_count
        }

    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.post('/create')
async def oquvchi_qoshish(form: CreateStudent, db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_student(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.put('/update_status')
async def statusni_tahrirlash(form: UpdateStatus, db: AsyncSession = Depends(get_database),
                               current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_status(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.put('/update')
async def oquvchi_tahrirlash(ident:int, form: UpdateStudent, db: AsyncSession = Depends(get_database),
                             current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_student(ident, form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@student_router.delete('/delete')
async def oquvchi_ochirish(ident:int, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_student(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))