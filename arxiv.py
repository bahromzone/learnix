
# async def get_total_payments_by_course(year: int, month: int, db, user):
#
#     if user.role not in ["admin", "boss"]:
#         raise HTTPException(status_code=403, detail="Sizga bu bo‘limni ko‘rishga ruxsat yo‘q!")
#
#     month_str = MONTH_NAMES.get(month)
#     if not month_str:
#         raise HTTPException(400, "Noto'g'ri oy kiritildi")
#
#     query = (
#         select(
#             Courses.id.label("course_id"),
#             Courses.name.label("course_name"),
#             func.coalesce(func.sum(Payment.amount), 0).label("total_amount"),
#             func.coalesce(func.sum(case((Payment.payment_type == "click", Payment.amount), else_=0)), 0).label("click_amount"),
#             func.coalesce(func.sum(case((Payment.payment_type == "cash", Payment.amount), else_=0)), 0).label("cash_amount"),
#         )
#         .join(Groups, Groups.course_id == Courses.id)
#         .join(Students, Students.group_id == Groups.id)
#         .join(Payment, Payment.student_id == Students.id)
#         .where(
#             extract('year', Payment.payment_date) == year,
#             Payment.month == month_str
#         )
#         .group_by(Courses.id, Courses.name)
#     )
#
#     result = await db.execute(query)
#     courses_total = result.all()
#
#     return [
#         {
#             "course_id": row.course_id,
#             "course_name": row.course_name,
#             "total_amount": row.total_amount or 0,
#             "click_amount": row.click_amount or 0,
#             "cash_amount": row.cash_amount or 0
#         }
#         for row in courses_total
#     ]