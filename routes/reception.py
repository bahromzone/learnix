from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.reception import create_reception, get_reception, delete_reception, get_reception_statistics, get_monthly_statistics, \
    get_total_students, update_reception
from routes.auth import get_current_active_user
from schemas.reception import CreateReception, UpdateReception
from schemas.users import CreateUser
from datetime import date


reception_router = APIRouter(
    prefix="/reception",
    tags=["Reception operation"]
)


@reception_router.get("/get")
async def qabuldagilarni_korish(year: int = None, month: int = None, db: AsyncSession = Depends(get_database),
                                current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await get_reception(year, month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.get("/get_statistics")
async def qabul_statistikasi(stat_date: date = None, db: AsyncSession = Depends(get_database),
                                current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await get_reception_statistics(stat_date, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.get("/get_monthly_statistics")
async def oylik_qabul_statistikasi(year: int = None, month: int = None, db: AsyncSession = Depends(get_database),
                                current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await get_monthly_statistics(year, month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.get("/get_total_reception_students")
async def oylik_qabullar_soni(year: int = None, month: int = None, db: AsyncSession = Depends(get_database),
                                current_user: CreateUser = Depends(get_current_active_user)):

    try:
        return await get_total_students(year, month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.post("/create")
async def qabulga_qoshish(form: CreateReception,db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_reception(form,db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.put("/update")
async def qabuldagilarni_tahrirlash(form: UpdateReception,db: AsyncSession = Depends(get_database),
                                    current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_reception(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@reception_router.delete("/delete")
async def qabuldagilarni_ochirish(ident: int, db: AsyncSession = Depends(get_database),
                                  current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_reception(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))
