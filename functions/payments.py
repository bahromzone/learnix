from sqlalchemy import case
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.expenses import get_sum_expense
from models.courses import Groups
from models.payments import Payment
from models.students import Students
from utils.db_operations import save_in_db, get_in_db
from sqlalchemy.sql import func, extract
from schemas.payments import PaymentType

MONTH_NAMES = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"
}


async def get_all_payments(course_id,db, user):

    if user.role not in ["admin", "boss"]:
        raise HTTPException(status_code=403, detail="Sizga barcha to‘lovlarni ko‘rishga ruxsat yo‘q!")

    query = (
        select(
            Payment.id,
            Students.full_name.label("student_name"),
            Groups.name.label("group_name"),
            Payment.month,
            Payment.amount,
            Payment.payment_persent
        )
        .select_from(Payment)
        .join(Students, Students.id == Payment.student_id)
        .join(Groups, Groups.id == Payment.group_id)
    )

    if course_id is not None:
        query = query.where(Groups.course_id == course_id)

    query = query.order_by(Payment.id.desc())

    result = await db.execute(query)
    payments = result.mappings().all()

    return payments


async def get_sum_payment(year, month, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    if not (1 <= month <= 12):
        raise HTTPException(400, "Oy 1 dan 12 gacha bo'lishi kerak")

    month_str = MONTH_NAMES.get(month)
    if not month_str:
        raise HTTPException(400, "Noto'g'ri oy kiritildi")

    cash_payment = func.sum(case((Payment.payment_type == 'cash', Payment.amount), else_=0))
    click_payment = func.sum(case((Payment.payment_type == 'click', Payment.amount), else_=0))
    total_expense = func.sum(Payment.amount)

    query = select(cash_payment, click_payment, total_expense).filter(
        extract('year', Payment.payment_date) == year,
        Payment.month == month_str
    )

    result = await db.execute(query)
    cash, click, total = result.first()

    return {
        "year": year,
        "month": month,
        "cash_payment": cash or 0,
        "click_payment": click or 0,
        "total_expense": total or 0
    }


async def get_profit(year: int, month: int, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    income_data = await get_sum_payment(year, month, db, user)
    total_income = income_data['total_expense']
    cash_income = income_data['cash_payment']
    click_income = income_data['click_payment']

    expense_data = await get_sum_expense(year, month, db, user)
    total_expense = expense_data['total_expense']
    cash_expense = expense_data['cash_expense']
    click_expense = expense_data['click_expense']

    profit = total_income - total_expense
    cash_profit = cash_income - cash_expense
    click_profit = click_income - click_expense

    return {
        "year": year,
        "month": month,
        "cash_profit": cash_profit or 0,
        "click_profit": click_profit or 0,
        "total_profit": profit or 0
    }

async def get_teacher_payments(db, user):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Sizga bu bo‘limni ko‘rishga ruxsat yo‘q!")

    if not user.group_ids:
        return []

    query = (
        select(Payment)
        .where(Payment.group_id.in_(tuple(user.group_ids)))
        .options(joinedload(Payment.student), joinedload(Payment.group))
    )

    result = await db.execute(query)
    payments = result.scalars().all()

    return payments


async def create_payment(form, db, user):

    if user.role not in ["admin", "boss"]:
        raise HTTPException(status_code=403, detail="Sizga to'lov qo'shishga ruxsat yo'q!")

    student = await get_in_db(db, Students, form.student_id)
    await get_in_db(db, Groups, form.group_id)

    if student.discount == 100:
         raise HTTPException(status_code=400, detail="Grant o'quvchi tolov qilmaydi !!! ")

    if student.discount > 0 and form.discount>0:
        raise HTTPException(status_code=400, detail="O'quvchi 1 ta chegirmadan foydalanishi mumkin xolos !!! ")

    stmt = select(Payment).where(
        Payment.student_id == form.student_id,
        Payment.group_id == form.group_id,
        Payment.month == form.month
    )
    result = await db.execute(stmt)
    existing_payment = result.scalar_one_or_none()


    if existing_payment:
        existing_payment.amount += form.amount
        existing_payment.payment_persent = (existing_payment.amount * 100) / student.payment_amount
        existing_payment.payment_date = form.payment_date
        await db.commit()
        await db.refresh(existing_payment)
        return {
            "message": "To‘lov muvaffaqiyatli yangilandi!",
         }

    else:
        new_payment = Payment(
            student_id=form.student_id,
            group_id=form.group_id,
            amount=form.amount,
            payment_type=form.payment_type,
            payment_date=form.payment_date,
            month=form.month,
            payment_persent=(form.amount*100) / (student.payment_amount - student.payment_amount*form.discount/100),
        )
        await save_in_db(db, new_payment)

        return {
            "message": "Yangi to‘lov muvaffaqiyatli qo‘shildi!",
        }


async def update_payment(ident, form, db, user):
    if user.role not in ["admin", "boss"]:
        raise HTTPException(status_code=403, detail="Sizga to'lovni o'zgartirishga ruxsat yo'q!")

    result = await db.execute(select(Payment).where(Payment.id == ident))
    payment = result.scalar()

    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi!")

    if payment.payment_type == PaymentType.CLICK:
        raise HTTPException(status_code=400, detail="Click orqali qilingan to‘lov o‘zgartirilmaydi!")

    payment.amount = form.amount
    payment.payment_type = form.payment_type

    await db.commit()
    await db.refresh(payment)

    return {"message": "To‘lov muvaffaqiyatli yangilandi!", "payment_id": payment.id}


async def delete_payment(ident, db, user):
    if user.role not in ["admin", "boss"]:
        raise HTTPException(status_code=403, detail="Sizga to'lovni o'chirishga ruxsat yo'q!")

    result = await db.execute(select(Payment).where(Payment.id == ident))
    payment = result.scalar()

    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi!")

    await db.delete(payment)
    await db.commit()

    return {"message": "To‘lov muvaffaqiyatli o‘chirildi!"}