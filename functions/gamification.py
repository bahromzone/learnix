from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func, case
from sqlalchemy.ext.asyncio import AsyncSession
from models.students import Students
from models.attendances import Attendance

# --- Konfiguratsiya ---
POINTS_PER_PRESENT = 10

# (min_ball, daraja_nomi) - o'sish tartibida
LEVELS = [
    (0, "Yangi"),
    (100, "O'quvchi"),
    (300, "Tirishqoq"),
    (600, "Zo'r"),
    (1000, "Chempion"),
]


def get_level(points: int):
    """Ballga qarab daraja raqami, nomi va keyingi darajagacha qolgan ballni qaytaradi."""
    level = 1
    name = LEVELS[0][1]
    next_threshold = None
    for i, (threshold, nm) in enumerate(LEVELS):
        if points >= threshold:
            level = i + 1
            name = nm
            next_threshold = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    points_to_next = (next_threshold - points) if next_threshold is not None else None
    return level, name, next_threshold, points_to_next


def build_badges(present: int, total: int, rate: float):
    """Statistikaga qarab olingan nishonlar ro'yxati."""
    badges = []
    if present >= 1:
        badges.append({"code": "first_step", "name": "Ilk qadam", "description": "Birinchi darsga qatnashdi"})
    if present >= 10:
        badges.append({"code": "active", "name": "Faol o'quvchi", "description": "10 marta darsga keldi"})
    if present >= 50:
        badges.append({"code": "star", "name": "Yulduz", "description": "50 marta darsga keldi"})
    if present >= 100:
        badges.append({"code": "legend", "name": "Afsona", "description": "100 marta darsga keldi"})
    if total >= 5 and rate == 100.0:
        badges.append({"code": "perfect", "name": "Mukammal davomat", "description": "100% davomat (kamida 5 dars)"})
    return badges


def _compose(student_id, full_name, present, total):
    present = int(present or 0)
    total = int(total or 0)
    points = present * POINTS_PER_PRESENT
    rate = round((present / total) * 100, 1) if total else 0.0
    level, level_name, next_threshold, points_to_next = get_level(points)
    return {
        "student_id": student_id,
        "full_name": full_name,
        "points": points,
        "level": level,
        "level_name": level_name,
        "next_level_at": next_threshold,
        "points_to_next_level": points_to_next,
        "present_count": present,
        "total_sessions": total,
        "attendance_rate": rate,
        "badges": build_badges(present, total, rate),
    }


async def get_student_gamification(student_id: int, db: AsyncSession, user):
    result = await db.execute(select(Students).where(Students.id == student_id))
    student = result.scalar()
    if not student:
        raise HTTPException(404, "O'quvchi topilmadi")

    present_expr = func.coalesce(
        func.sum(case((Attendance.status.is_(True), 1), else_=0)), 0
    )
    total_expr = func.count(Attendance.id)

    stats = await db.execute(
        select(present_expr, total_expr).where(Attendance.student_id == student_id)
    )
    present, total = stats.first()
    return _compose(student.id, student.full_name, present, total)


async def get_leaderboard(limit: int, group_id, db: AsyncSession, user):
    present_expr = func.coalesce(
        func.sum(case((Attendance.status.is_(True), 1), else_=0)), 0
    ).label("present")
    total_expr = func.count(Attendance.id).label("total")

    query = (
        select(
            Students.id,
            Students.full_name,
            present_expr,
            total_expr,
        )
        .outerjoin(Attendance, Attendance.student_id == Students.id)
        .where(Students.status == "active")
        .group_by(Students.id)
        .order_by(present_expr.desc(), Students.id)
        .limit(limit)
    )

    if group_id:
        query = query.where(Students.group_id == group_id)

    result = await db.execute(query)
    rows = result.fetchall()

    leaderboard = []
    for rank, row in enumerate(rows, start=1):
        entry = _compose(row.id, row.full_name, row.present, row.total)
        entry["rank"] = rank
        leaderboard.append(entry)
    return leaderboard
