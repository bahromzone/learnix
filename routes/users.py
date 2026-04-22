from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from functions.users import get_all_teacher, delete_user, user_image, \
    create_user_with_role, update_profil, get_own, \
    logout_user, get_all_user, delete_teacher, update_teacher
from models.users import Users
from routes.auth import get_current_active_user
from schemas.users import CreateUser, UpdateUser
from db import get_database
from sqlalchemy.future import select


user_router = APIRouter(
    prefix="/user",
    tags=["User operation"]
)

admistrator_router = APIRouter(
    prefix="/admistrator",
    tags=["Boss vs Admin operation"]
)


@admistrator_router.get('/get_all')
async def barcha_xodimlarni_korish(db: AsyncSession = Depends(get_database),
                                 current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_user(db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@admistrator_router.get('/get_all_teacher')
async def barcha_oqituvchilarni_korish(db: AsyncSession = Depends(get_database),
                                 current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_all_teacher(db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@admistrator_router.get('/get_all_teacher_count')
async def oqituvchilarni_soni(db: AsyncSession = Depends(get_database),
                              current_user: CreateUser = Depends(get_current_active_user)):

    try:
        if current_user.role not in ['admin', 'boss']:
            raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

        result = await db.execute(select(Users).filter(Users.role == 'teacher'))
        teacher_count = len(result.scalars().all())
        return {"count": teacher_count}

    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.get('/get_own')
async def profil(db: AsyncSession = Depends(get_database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_own(db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))



@admistrator_router.post('/create_teacher')
async def oqituvchi_qoshish(form: CreateUser, db: AsyncSession = Depends(get_database),
                                               current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_user_with_role(form, db, current_user, role="teacher")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@admistrator_router.post('/create_admin')
async def admin_qoshish(form: CreateUser, db: AsyncSession = Depends(get_database),
                                      current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_user_with_role(form, db, current_user, role="admin")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@admistrator_router.post('/create_boss')
async def boss_qoshish(form: CreateUser, db: AsyncSession = Depends(get_database),
                                      current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await create_user_with_role(form, db, current_user, role="boss")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.post('/upload-image')
async def profilga_rasm_yuklash(file: UploadFile = File(...),
                                  db: AsyncSession = Depends(get_database),
                                  current_user: CreateUser = Depends(get_current_active_user)):
    try:
        await user_image(file, db, current_user)
        return {"message": "Rasm muvaffaqiyatli yuklandi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@admistrator_router.put("/update_user")
async def oqituvchini_tahrirlash(ident:int, form: UpdateUser, db: AsyncSession = Depends(get_database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_teacher(ident, form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.put("/update_own")
async def profil_tahrirlash(form: UpdateUser, db: AsyncSession = Depends(get_database),
                                        current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await update_profil(form, db, current_user)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@admistrator_router.delete("/delete_user")
async def xodimlarni_ochirish(ident: int = 0, db: AsyncSession = Depends(get_database),
                              current_user: CreateUser = Depends(get_current_active_user)):
    try:
        await delete_user(ident, db, current_user)
        return {"message": "Xodim o'chirildi !"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))



@admistrator_router.delete("/delete_teacher")
async def oqituvchilarni_ochirish(ident: int = 0, db: AsyncSession = Depends(get_database),
                                  current_user: CreateUser = Depends(get_current_active_user)):
    try:
        await delete_teacher(ident, db, current_user)
        return {"message": "O'qituvchi o'chirildi !"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.delete("/delete_own")
async def logout(db: AsyncSession = Depends(get_database),
                     current_user: CreateUser = Depends(get_current_active_user)):
    try:
        await logout_user(db, current_user)
        return {"message": "Logout qilindi!"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))