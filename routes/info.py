from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.info import get_info, update_info, create_info, delete_info
from routes.auth import get_current_active_user
from schemas.info import SchemaInfo
from schemas.users import CreateUser


info_router = APIRouter(
    prefix="/info",
    tags=["Info operation"]
)


@info_router.get("/get")
async def qoshimcha_malumotlarni_korish(student_id: int = None, db: AsyncSession = Depends(get_database),
                         user: CreateUser = Depends(get_current_active_user)):
    return await get_info(student_id,db, user)


@info_router.post("/create")
async def qoshimcha_malumotlarni_qoshish(form: SchemaInfo, db: AsyncSession = Depends(get_database),
                            user: CreateUser = Depends(get_current_active_user)):
    return await create_info(form, db, user)


@info_router.put("/update")
async def qoshimcha_malumotlarni_tahrirlash(ident: int, form: SchemaInfo, db: AsyncSession = Depends(get_database),
                                            user: CreateUser = Depends(get_current_active_user)):
    return await update_info(ident, form, db, user)


@info_router.delete("/delete")
async def qoshimcha_malumotlarni_ochirish(ident: int, db: AsyncSession = Depends(get_database),
                                          user: CreateUser = Depends(get_current_active_user)):
    return await delete_info(ident, db, user)

