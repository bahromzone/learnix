from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.expenditures import create_expense, update_expense, delete_expense, get_all_expense, get_sum_expense
from routes.auth import get_current_active_user
from schemas.expenditures import CreateExpense, UpdateExpense
from schemas.users import CreateUser
from datetime import date


expense_router = APIRouter(
    prefix="/expense",
    tags=["Expense operation"]
)


@expense_router.get("/get")
async def barcha_xarajatlarni_korish(start_date: date = None, end_date: date = None, expense_type: str = None,
                                     db: AsyncSession =Depends(get_database),
                                     current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_expense(start_date, end_date, expense_type, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@expense_router.get("/get_sum_expense")
async def barcha_xarajatlar_summasi(year:int = None, month:int = None, db: AsyncSession = Depends(get_database),
                                      current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_sum_expense(year, month, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@expense_router.post("/create")
async def xarajat_qoshish(form: CreateExpense, db: AsyncSession = Depends(get_database),
                          current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_expense(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@expense_router.put("/update")
async def xarajat_tahrirlash(form: UpdateExpense, db: AsyncSession = Depends(get_database),
                             current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_expense(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@expense_router.delete("/delete")
async def xarajat_ochirish(ident:int, db: AsyncSession = Depends(get_database),
                           current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await delete_expense(ident, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))