from fastapi import HTTPException
from models.courses import Courses, Groups
from models.students import Students
from models.users import Users
from utils.db_operations import save_in_db, get_in_db
from sqlalchemy.future import select
from sqlalchemy import delete, update, func, and_
from utils.save_image import save_image


async def get_all_course(db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    query = select(Courses).order_by(Courses.id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_course(course_name, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    course = Courses(name = course_name)
    await save_in_db(db, course)
    return {"message": "Kurs muvaffaqiyatli yaratildi", "id": course.id}


async def update_course(ident, new_name, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")

    c_result = await db.execute(select(Courses).where(Courses.id == ident))
    course = c_result.scalar()

    if not course:
        raise HTTPException(404, "Kurs topilmadi")

    course.name = new_name
    await db.commit()
    return {"message": "Kurs muvaffaqiyatli tahrirlandi"}


async def course_images(ident, file, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    image_filename = await save_image(file)

    async with db as session:
        result = await session.execute(select(Courses).filter(Courses.id == ident))
        course = result.scalar()

        if not course:
            raise HTTPException(404, "Kurs topilmadi")

        course.image = image_filename
        await session.commit()
        return {"message": "Rasm muvaffaqiyatli yuklandi"}


async def delete_course(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Courses, ident)

    await db.execute(delete(Courses).where(Courses.id == ident))

    await db.commit()
    return {"message": "Kurs va unga oid guruhlar va studentlar hammasi o'chirildi"}



async def get_all_group(course_id, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    query = (
        select(
            Groups.id,
            Groups.name,
            Groups.course_id,
            Groups.price,
            Groups.period,
            Groups.status,
            func.count(Students.id).label("student_count")
        )
        .outerjoin(
            Students,
            and_(
                Students.group_id == Groups.id,
                Students.status == "active"
            )
        )
        .filter(Groups.status == "active")
        .group_by(Groups.id)
        .order_by(Groups.id)
    )

    if course_id:
        query = query.filter(Groups.course_id == course_id)

    result = await db.execute(query)
    rows = result.fetchall()

    return [
        {
            "id": row.id,
            "name": row.name,
            "price": row.price,
            "period": row.period,
            "status": row.status,
            "course_id": row.course_id,
            "student_count": row.student_count
        }
        for row in rows
    ]


async def create_group(form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Courses).filter(Courses.id == form.course_id))
    course = result.scalar()

    if not course:
        raise HTTPException(404, "Kurs topilmadi")

    teacher_result = await db.execute(select(Users).filter(Users.id == form.teacher_id))
    teacher = teacher_result.scalar()

    if not teacher:
        raise HTTPException(404, "Teacher topilmadi")

    new_group = Groups(
        name = form.name,
        period = form.period,
        price = form.price,
        course_id = form.course_id,
        teacher_id = form.teacher_id,
        status = 'active'
    )
    await save_in_db(db, new_group)
    return {"message": "Guruh muvaffaqiyatli yaratildi", "id": new_group.id}


async def update_group_status(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Groups, ident)

    await db.execute(update(Groups).filter(Groups.id == ident).values(status='finished'))
    await db.commit()
    return {"message": "Guruh statusi muvaffaqiyatli tahrirlandi"}


async def update_group(ident, form, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Groups, ident)

    await db.execute(update(Groups).filter(Groups.id == ident).values(**form.dict()))
    await db.commit()
    return {"message": "Guruh muvaffaqiyatli tahrirlandi"}


async def delete_group(ident, db, user):

    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    await get_in_db(db, Groups, ident)

    await db.execute(delete(Groups).where(Groups.id == ident))

    await db.commit()
    return {"message": "Guruh va unga oid studentlar hammasi o'chirildi"}

    