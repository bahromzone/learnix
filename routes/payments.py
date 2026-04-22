from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.payments import create_payment, update_payment, delete_payment, get_all_payments, get_teacher_payments, get_sum_payment, get_profit
from routes.auth import get_current_active_user
from schemas.payments import PaymentCreate, PaymentUpdate
from schemas.users import CreateUser


payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment operation"]
)


@payment_router.get('/profit')
async def oylik_foyda_hisoboti(year:int = None, month:int = None, db:AsyncSession = Depends(get_database),
                               current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_profit(year, month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@payment_router.get('/all')
async def barcha_tolovlar(course_id: int = None,db: AsyncSession = Depends(get_database), current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_payments(course_id, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@payment_router.get('/monthly_sum')
async def umumiy_tolovlar_summasi(year:int = None, month:int = None, db: AsyncSession = Depends(get_database),
                                   current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_sum_payment(year, month,db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@payment_router.get('/for_teacher')
async def tolovlar(db: AsyncSession = Depends(get_database),
                                   current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_teacher_payments(db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@payment_router.post('/create')
async def tolov_qilish(form: PaymentCreate, db: AsyncSession = Depends(get_database),
                             current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_payment(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@payment_router.put('/update')
async def tolov_tahrirlash(ident:int, form: PaymentUpdate, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_payment(ident, form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))



@payment_router.delete('/delete')
async def tolov_ochirish(ident:int, db: AsyncSession = Depends(get_database),
                         current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_payment(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))