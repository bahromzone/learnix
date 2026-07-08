from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import Users
from models.courses import Courses, Groups
from models.students import Students


async def get_instructor_profile(ident: int, db: AsyncSession):
    # Faqat 'teacher' rolidagi foydalanuvchini instruktor deb hisoblaymiz
    result = await db.execute(
        select(Users).where(Users.id == ident, Users.role == "teacher")
    )
    teacher = result.scalar()

    if not teacher:
        raise HTTPException(404, "O'qituvchi topilmadi")

    # Instruktorning aktiv guruhlari + kurs nomi + aktiv student soni
    query = (
        select(
            Groups.id,
            Groups.name,
            Groups.period,
            Groups.status,
            Courses.id.label("course_id"),
            Courses.name.label("course_name"),
            func.count(Students.id).label("student_count"),
        )
        .join(Courses, Courses.id == Groups.course_id)
        .outerjoin(
            Students,
            and_(Students.group_id == Groups.id, Students.status == "active"),
        )
        .where(Groups.teacher_id == ident, Groups.status == "active")
        .group_by(Groups.id, Courses.id)
        .order_by(Groups.id)
    )
    result = await db.execute(query)
    rows = result.fetchall()

    groups = [
        {
            "id": row.id,
            "name": row.name,
            "period": row.period,
            "status": row.status,
            "course_id": row.course_id,
            "course_name": row.course_name,
            "student_count": row.student_count,
        }
        for row in rows
    ]

    # Takrorlanmas kurslar ro'yxati
    courses = {}
    for g in groups:
        courses[g["course_id"]] = g["course_name"]

    return {
        "id": teacher.id,
        "full_name": teacher.full_name,
        "image": teacher.image,
        "courses": [{"id": cid, "name": name} for cid, name in courses.items()],
        "groups": groups,
        "total_groups": len(groups),
        "total_students": sum(g["student_count"] for g in groups),
    }
