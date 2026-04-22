from fastapi import HTTPException
from sqlalchemy import select
from models.attendances import Attendance
from models.courses import Groups
from models.students import Students
from utils.db_operations import save_in_db
from sqlalchemy.orm import joinedload


async def get_student_attendance_stats(student_id, db, user):
    if user.role in ['admin', 'boss']:
        query = select(Attendance).options(joinedload(Attendance.student)).join(Students, Attendance.student_id == Students.id)

        if student_id:
            query = query.where(Attendance.student_id == student_id)

        result = await db.execute(query)
        attendance_data = result.scalars().all()

        stats = []
        for attendance in attendance_data:
            total_classes = len(attendance_data)
            present_classes = sum(1 for a in attendance_data if a.status == True)
            absent_classes = total_classes - present_classes
            attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
            stats.append({
                "student_id": attendance.student.id,
                "student_name": attendance.student.full_name,
                "total_classes": total_classes,
                "present_classes": present_classes,
                "absent_classes": absent_classes,
                "attendance_percentage": round(attendance_percentage, 2)
            })

        return stats

    elif user.role == 'teacher':
        query = (
            select(Attendance)
            .options(joinedload(Attendance.student))
            .join(Students, Attendance.student_id == Students.id)
            .join(Groups, Attendance.group_id == Groups.id)
            .where(Groups.teacher_id == user.id)
        )

        if student_id:
            query = query.where(Attendance.student_id == student_id)

        result = await db.execute(query)
        attendance_data = result.scalars().all()

        stats = []
        for attendance in attendance_data:
            total_classes = len(attendance_data)
            present_classes = sum(1 for a in attendance_data if a.status == True)
            absent_classes = total_classes - present_classes
            attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
            stats.append({
                "student_id": attendance.student.id,
                "student_name": attendance.student.full_name,
                "total_classes": total_classes,
                "present_classes": present_classes,
                "absent_classes": absent_classes,
                "attendance_percentage": round(attendance_percentage, 2)
            })

        return stats

    raise HTTPException(403, "Faqat admin, boss yoki teacher uchun!")



async def get_attendance_for_admin(attendance_date, teacher_id, group_id, student_id, db, user):
    if user.role not in ['admin', 'boss']:
        raise HTTPException(403, "Faqat admin va boss uchun!")

    query = (
        select(Attendance).options(joinedload(Attendance.student))
        .join(Students, Attendance.student_id == Students.id)
        .join(Groups, Attendance.group_id == Groups.id)
    )

    if attendance_date:
        query = query.where(Attendance.date == attendance_date)

    if teacher_id:
        query = query.where(Groups.teacher_id == teacher_id)

    if group_id:
        query = query.where(Attendance.group_id == group_id)

    if student_id:
        query = query.where(Attendance.student_id == student_id)

    result = await db.execute(query)
    return result.scalars().all()



async def get_attendance_for_teacher(attendance_date, group_id, student_id, db, user):

    if user.role != 'teacher':
        raise HTTPException(403, "Faqat o‘qituvchilar uchun!")

    query = (
        select(Attendance).options(joinedload(Attendance.student))
        .join(Students, Attendance.student_id == Students.id)
        .join(Groups, Attendance.group_id == Groups.id)
        .where(Groups.teacher_id == user.id)
    )

    if attendance_date:
        query = query.where(Attendance.date == attendance_date)

    if group_id:
        query = query.where(Attendance.group_id == group_id)

    if student_id:
        query = query.where(Attendance.student_id == student_id)


    result = await db.execute(query)
    return result.scalars().all()



async def create_attendance(form, db, user):

    if user.role != "teacher":
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    s_result = await db.execute(select(Students).where(Students.id == form.student_id))
    student = s_result.scalar()

    if not student:
        raise HTTPException(404, "Bunday student mavjud emas!")

    c_result = await db.execute(select(Groups).where(Groups.id == form.group_id))
    group = c_result.scalar()

    if not group:
        raise HTTPException(404, "Bunday guruh mavjud emas!")

    if group.teacher_id != user.id:
        raise HTTPException(403, "Siz ushbu o'quvchi uchun davomat ola olmaysiz!")

    if student.group_id != form.group_id:
        raise HTTPException(400, "Bu o'quvchi ushbu guruhga yozilmagan!")

    att_result = await db.execute(
        select(Attendance).where(
            Attendance.student_id == form.student_id,
            Attendance.group_id == form.group_id,
            Attendance.date == form.date,
            Attendance.description == form.description
        )
    )
    existing_attendance = att_result.scalar()

    if existing_attendance:
        raise HTTPException(400, "Bu student uchun ushbu sanada allaqachon davomat olingan!")

    new_attendance = Attendance(**form.dict())
    await save_in_db(db, new_attendance)

    return {"message": "Davomat olindi", "student_id": new_attendance.student_id}



async def update_attendance(attendance_id, form, db, user):

    if user.role not in ['admin', 'teacher', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Attendance).where(Attendance.id == attendance_id))
    attendance = result.scalar()

    if not attendance:
        raise HTTPException(404, "Davomat topilmadi!")

    if user.role in ['teacher','admin', 'boss']:
        group_result = await db.execute(select(Groups).where(Groups.id == attendance.group_id))
        group = group_result.scalar()
        if not group or group.teacher_id != user.id:
            raise HTTPException(403, "Siz faqat o'z kurslaringizga tegishli davomatlarni o'zgartira olasiz!")

    s_result = await db.execute(select(Students).where(Students.id == form.student_id))
    student = s_result.scalar()
    if not student:
        raise HTTPException(404, "Bunday student mavjud emas!")

    c_result = await db.execute(select(Groups).where(Groups.id == form.group_id))
    group = c_result.scalar()
    if not group:
        raise HTTPException(404, "Bunday guruh mavjud emas!")

    attendance.date = form.date
    attendance.status = form.status
    attendance.student_id = form.student_id
    attendance.group_id = form.group_id
    attendance.description = form.description

    await save_in_db(db, attendance)

    return {"message": "Davomat yangilandi", "attendance_id": attendance.id}


async def delete_attendance(attendance_id, db, user):
    if user.role not in ['admin', 'teacher', 'boss']:
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    result = await db.execute(select(Attendance).where(Attendance.id == attendance_id))
    attendance = result.scalar()

    if not attendance:
        raise HTTPException(404, "Davomat topilmadi!")

    if user.role == 'teacher':
        group_result = await db.execute(select(Groups).where(Groups.id == attendance.group_id))
        group = group_result.scalar()
        if not group or group.teacher_id != user.id:
            raise HTTPException(403, "Siz faqat o'z kurslaringizning davomatlarini o'chira olasiz!")

    await db.delete(attendance)
    await db.commit()

    return {"message": "Davomat o'chirildi", "attendance_id": attendance_id}

