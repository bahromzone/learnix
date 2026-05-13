from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.presences import get_attendance_for_teacher, create_attendance, update_attendance, delete_attendance, \
    get_attendance_for_admin, get_student_attendance_stats
from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_active_user
from schemas.presences import CreateAttendance, UpdateAttendance
from schemas.users import CreateUser

attendance_router = APIRouter(
    prefix="/attendance",
    tags=["Attendance operation"]
)


@attendance_router.get('/get_attendances_statistics')
async def davomat_statistikasi(student_id: int = None, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_student_attendance_stats(student_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@attendance_router.get('/get_attendances_for_admins')
async def barcha_davomatni_korish(attendance_date:date = None, teacher_id:int = None, group_id: int = None, student_id: int = None, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_attendance_for_admin(attendance_date, teacher_id, group_id, student_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@attendance_router.get('/get_attendances_for_teachers')
async def davomatni_korish(attendance_date:date = None,group_id: int = None, student_id: int = None, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_attendance_for_teacher(attendance_date, group_id, student_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@attendance_router.post('/create')
async def davomat_qoshish(form: CreateAttendance, db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    try:
         return await create_attendance(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@attendance_router.put('/update')
async def davomat_tahrirlash(attendance_id:int, form: UpdateAttendance, db: AsyncSession = Depends(get_database),
                             current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_attendance(attendance_id, form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@attendance_router.delete('/delete')
async def davomat_ochirish(attendance_id:int, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_attendance(attendance_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))