from fastapi import HTTPException
from sqlalchemy import update, delete
from models.information import Info
from models.students import Students
from utils.db_control import save_in_db, get_in_db
from sqlalchemy.future import select

async def get_info(student_id, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    if student_id:
        query = select(Info).where(Info.student_id == student_id)
        result = await db.execute(query)
        return result.scalars().first()
    else:
        query = select(Info).order_by(Info.id)
        result = await db.execute(query)
        return result.scalars().all()


async def create_info(form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Students, form.student_id)

    new_info = Info(**form.dict())
    await save_in_db(db, new_info)
    return {"message": "Student uchun qo'shimcha ma'lumot muvaffaqiyatli yaratildi"}


async def update_info(ident, form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Info, ident)

    await db.execute(update(Info).filter(Info.id == ident).values(**form.dict()))
    await db.commit()
    return {"message": "Student uchun qo'shimcha ma'lumot muvaffaqiyatli tahrirlandi"}


async def delete_info(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Info, ident)

    await db.execute(delete(Info).filter(Info.id == ident))
    await db.commit()
    return {"message": "Student uchun qo'shimcha ma'lumot muvaffaqiyatli o'chirildi"}