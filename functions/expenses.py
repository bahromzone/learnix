from fastapi import HTTPException
from utils.db_control import save_in_db, get_in_db
from models.expenditures import Expenses
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.sql import func, extract, and_


async def get_sum_expense(year, month, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    query = select(func.sum(Expenses.amount)).filter(extract('year', Expenses.date) == year,
                                                     extract('month', Expenses.date) == month)
    result = await db.execute(query)
    total_expense = result.scalar() or 0

    cash_query = select(func.sum(Expenses.amount)).filter(extract('year', Expenses.date) == year,
                                                     extract('month', Expenses.date) == month,
                                                     Expenses.payment_type == 'cash')
    cash_result = await db.execute(cash_query)
    cash_expense = cash_result.scalar() or 0

    click_query = select(func.sum(Expenses.amount)).filter(extract('year', Expenses.date) == year,
                                                     extract('month', Expenses.date) == month,
                                                     Expenses.payment_type == 'click')
    click_result = await db.execute(click_query)
    click_expense = click_result.scalar() or 0



    return {
        "year": year,
        "month": month,
        "cash_expense": cash_expense,
        "click_expense": click_expense,
        "total_expense": total_expense
    }


async def get_all_expense(start_date, end_date, expense_type, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    query = select(Expenses).order_by(Expenses.id.desc())

    filters = []
    if expense_type:
        filters.append(Expenses.payment_type == expense_type)
    if start_date and end_date:
        filters.append(func.date(Expenses.date).between(start_date, end_date))

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    expenses = result.scalars().all()

    return [
        {
            "id": exp.id,
            "category": exp.category,
            "amount": exp.amount,
            "date": exp.date.strftime("%Y-%m-%d"),
            "payment_type": exp.payment_type,
            "description": exp.description
        }
        for exp in expenses
    ]



async def create_expense(form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    new_expense = Expenses(**form.dict())
    await save_in_db(db, new_expense)
    return {"message": "Xarajat ro'yxatga qo'shildi"}


async def update_expense(form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Expenses, form.ident)

    await db.execute(update(Expenses).filter(Expenses.id == form.ident).values(**form.dict()))
    await db.commit()
    return {"message": "Xarajat muvaffaqiyatli tahrirlandi"}


async def delete_expense(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Expenses, ident)

    await db.execute(delete(Expenses).filter(Expenses.id == ident))
    await db.commit()
    return {"message": "Xarajat ro'yxatdan o'chirildi"}