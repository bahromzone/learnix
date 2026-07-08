from fastapi import APIRouter
from routes.auth import login_router
from routes.users import user_router, admistrator_router
from routes.courses import course_router, group_router
from routes.students import student_router
from routes.attendances import attendance_router
from routes.payments import payment_router
from routes.reception import reception_router
from routes.expenses import expense_router
from routes.info import info_router
from routes.instructors import instructor_router

api = APIRouter()

api.include_router(reception_router)
api.include_router(attendance_router)
api.include_router(expense_router)
api.include_router(payment_router)
api.include_router(info_router)
api.include_router(student_router)
api.include_router(course_router)
api.include_router(group_router)
api.include_router(admistrator_router)
api.include_router(user_router)
api.include_router(instructor_router)
api.include_router(login_router)
