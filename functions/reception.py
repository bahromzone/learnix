from fastapi import HTTPException
from sqlalchemy import update, delete, func, extract
from sqlalchemy.future import select
from models.reception import Reception
from utils.db_operations import save_in_db, get_in_db


async def get_reception_statistics(stat_date, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    query = select(
        Reception.course,
        func.count(Reception.id).label("student_count")
    ).group_by(Reception.course).order_by(func.count(Reception.id).desc())

    if stat_date:
        query = query.filter(Reception.visit_date == stat_date)

    result = await db.execute(query)
    stats = result.all()

    return [{"course": course, "students": count} for course, count in stats]


async def get_monthly_statistics(year, month, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    query = (select(
        Reception.course,
        func.count(Reception.id).label("student_count")
    ).filter(extract('year', Reception.visit_date) == year,
             extract('month', Reception.visit_date) == month)
             .group_by(Reception.course)
             .order_by(func.count(Reception.id).desc()))

    result = await db.execute(query)
    stats = result.fetchall()

    return {
        "year": year,
        "month": month,
        "statistics": [{"course": course, "students": count} for course, count in stats]
    }



async def get_total_students(year, month, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    query = (
        select(func.count(Reception.id))
        .where(
            extract('year', Reception.visit_date) == year,
            extract('month', Reception.visit_date) == month
        )
    )

    result = await db.execute(query)
    total_students = result.scalar()

    return {
        "year": year,
        "month": month,
        "total_students": total_students
    }


async def get_reception(year, month, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    query = select(Reception).order_by(Reception.id.desc())
    if year:
        query = query.where(extract('year', Reception.visit_date) == year)
    if month:
        query = query.where(extract('month', Reception.visit_date) == month)

    result = await db.execute(query)
    return result.scalars().all()


async def create_reception(form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    new_reception = Reception(**form.dict())
    await save_in_db(db, new_reception)
    return {"message": "Talaba ro'yxatga qo'shildi"}


async def update_reception(form, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Reception).filter(Reception.id == form.id))
    reception = result.scalar()

    if reception is None:
        raise HTTPException(404, "Bunday talaba mavjud emas!")

    await db.execute(update(Reception).filter(Reception.id == form.id).values(**form.dict()))
    await db.commit()
    return {"message": "Talaba muvaffaqiyatli tahrirlandi"}


async def delete_reception(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Reception, ident)

    await db.execute(delete(Reception).filter(Reception.id == ident))
    await db.commit()
    return {"message": "Talaba ro'yxatdan o'chirildi"}