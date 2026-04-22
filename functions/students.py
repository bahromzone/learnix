from fastapi import HTTPException
from sqlalchemy import update, delete, func, extract, or_, and_
from sqlalchemy.future import select
from models.courses import Groups
from models.payments import Payment
from models.students import Students
from utils.db_operations import save_in_db, get_in_db


async def get_debtors_by_year_month(year, month, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    payment_subquery = (
        select(
            Payment.student_id,
            func.sum(Payment.amount).label("total_paid"),
            func.max(Payment.payment_persent).label("max_payment_percent")
        )
        .where(
            and_(
                extract('year', Payment.payment_date) == year,
                Payment.month == month
            )
        )
        .group_by(Payment.student_id)
        .subquery()
    )

    stmt = (
        select(Students, payment_subquery.c.total_paid,
               payment_subquery.c.max_payment_percent)
        .outerjoin(payment_subquery,
                   Students.id == payment_subquery.c.student_id)
        .where(
            and_(
                Students.status == "active"),
                or_(
                    payment_subquery.c.max_payment_percent.is_(None),
                    payment_subquery.c.max_payment_percent < 100
                )
        )
    )

    result = await db.execute(stmt)
    rows = result.all()

    student_balances = []
    for student, total_paid, max_payment_percent in rows:
        total_paid = total_paid or 0
        max_payment_percent = max_payment_percent or 0

        remaining_percent = 100 - max_payment_percent
        remaining_amount = student.payment_amount - total_paid
        student_balances.append({
            "student_id": student.id,
            "student_name": student.full_name,
            "total_paid": total_paid,
            "remaining_percent": remaining_percent,
            "remaining_amount": remaining_amount
        })

    return student_balances


async def get_all_students(group_id, status, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    query = select(Students).order_by(Students.id)

    filters = []

    if group_id is not None:
        filters.append(Students.group_id == group_id)

    if status is not None:
        filters.append(Students.status == status)
    else:
        filters.append(Students.status == "active")

    query = query.where(*filters)

    result = await db.execute(query)
    return result.scalars().all()


async def get_own_student(group_id, db, user):
    if group_id:
        query = (select(Students).join(Groups, Groups.id == Students.group_id)
                 .filter(Groups.teacher_id == user.id, Students.group_id == group_id, Students.status == "active"))
        result = await db.execute(query)
        return result.scalars().all()
    else:
        query = (select(Students).join(Groups, Groups.id == Students.group_id)
                 .filter(Groups.teacher_id == user.id, Students.status == "active"))
        result = await db.execute(query)
        return result.scalars().all()


async def create_student(form,db,user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Groups).where(Groups.id == form.group_id))
    group = result.scalar()

    if group is None:
        raise HTTPException(404, "Bunday guruh mavjud emas !")

    new_student = Students(
        full_name=form.full_name,
        group_id=form.group_id,
        phone_number=form.phone_number,
        started_date=form.started_date,
        status="active",
        discount=form.discount,
        payment_amount = group.price - (group.price * form.discount / 100)
    )
    await save_in_db(db, new_student)
    return {"message": "O'quvchi muvaffaqiyatli yaratildi", "id": new_student.id}


async def update_status(form, db, current_user):
    if current_user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Students).where(Students.id == form.student_id))
    student = result.scalar()

    if student is None:
        raise HTTPException(404, "Bunday o'quvchi mavjud emas !")

    await db.execute(update(Students).where(Students.id == form.student_id).values(
        status=form.status
    ))
    await db.commit()
    return {"message": "O'quvchi statusi muvaffaqiyatli o'zgartirildi"}


async def update_student(ident, form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Students).where(Students.id == ident))
    student = result.scalar()

    if student is None:
        raise HTTPException(404, "Bunday o'quvchi mavjud emas !")

    result = await db.execute(select(Groups).where(Groups.id == form.group_id))
    group = result.scalar()

    if group is None:
        raise HTTPException(404, "Bunday guruh mavjud emas !")

    await db.execute(
        update(Students).where(Students.id == ident).values(
            full_name=form.full_name,
            group_id=form.group_id,
            phone_number=form.phone_number,
            started_date=form.started_date
        )
    )
    await db.commit()
    return {"message": "O'quvchi muvaffaqiyatli tahrirlandi"}


async def delete_student(ident,db,user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db,Students,ident)

    await db.execute(delete(Students).where(Students.id == ident))
    await db.commit()
    return {"message": "O'quvchi o'chirildi !"}