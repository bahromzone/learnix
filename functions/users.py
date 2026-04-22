from models.courses import Courses
from routes.auth import get_password_hash
from utils.db_operations import save_in_db
from models.users import Users
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from utils.save_image import save_image


async def user_image(file, db: AsyncSession, user) -> None:

    image_filename = await save_image(file)

    result = await db.execute(select(Users).filter(Users.id == user.id))
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")

    user.image = image_filename
    await db.commit()


async def get_all_user(db: AsyncSession, user):
    if user.role == 'boss':
        result = await db.execute(select(Users))
        return result.scalars().all()
    else:
        return []


async def get_own_group(db: AsyncSession, user):
    result = await db.execute(select(Courses).filter(Courses.teacher_id == user.id))
    group = result.scalars().all()
    if not group:
        return []
    return group


async def get_all_teacher(db: AsyncSession, user):
    if user.role in ['admin', 'boss']:
        result = await db.execute(select(Users).where(Users.role == 'teacher'))
        return result.scalars().all()
    else:
        return []


async def get_own(db: AsyncSession, user):
    result = await db.execute(select(Users).filter(Users.id == user.id))
    return result.scalars().first()


async def create_user_with_role(form, db: AsyncSession, current_user, role: str):
    result = await db.execute(select(Users).filter(Users.email == form.email))
    user_exists = result.scalar()
    if user_exists:
        raise HTTPException(400, "Bunday login avval ro`yxatga olingan!")

    if current_user.role != "boss":
        raise HTTPException(403, "Bu amalni bajarishga ruxsat yo'q!")

    new_user = Users(
        full_name=form.full_name,
        role=role,
        password=get_password_hash(form.password),
        email=form.email,
        phone_number=form.phone_number
    )
    await save_in_db(db, new_user)

    return {"message": f"{role.capitalize()} yaratildi.", "user_id": new_user.id}


async def update_teacher(ident, form, db: AsyncSession, user):
    new_user = await db.execute(select(Users).filter(Users.email == form.email))
    result = new_user.scalar()

    if result and result.id != user.id:
        raise HTTPException(400, "Bunday login avval ro`yxatga olingan!")

    await db.execute(
        update(Users).where(Users.id == ident).values(
            full_name=form.full_name,
            password=get_password_hash(form.password),
            email=form.email,
            phone_number=form.phone_number
        )
    )
    await db.commit()
    return {"message": "O'qituvchi tahrirlandi"}



async def update_profil(form, db: AsyncSession, user):

    new_user = await db.execute(select(Users).filter(Users.email == form.email))
    result = new_user.scalar()

    if result and result.id != user.id:
        raise HTTPException(400, "Bunday login avval ro`yxatga olingan!")


    await db.execute(
        update(Users).where(Users.id == user.id).values(
            full_name=form.full_name,
            password=get_password_hash(form.password),
            email=form.email,
            phone_number=form.phone_number
        )
    )
    await db.commit()
    return {"message": f"{user.role.capitalize()} tahrirlandi"}


async def delete_user(ident: int, db: AsyncSession, user):
    query = select(Users).where(Users.id == ident)
    result = await db.execute(query)
    user_to_delete = result.scalar()

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User topilmadi")

    if user.role in ['admin', 'boss']:
        delete_query = delete(Users).where(Users.id == ident)
        await db.execute(delete_query)
        await db.commit()
    else:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")


async def delete_teacher(ident: int, db: AsyncSession, user):
    query = select(Users).where(Users.id == ident)
    result = await db.execute(query)
    user_to_delete = result.scalar()

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User topilmadi")
    if user_to_delete.role != 'teacher':
        raise HTTPException(status_code=400, detail="Bunday teacher mavjud emas!")

    if user.role in ['admin', 'boss']:
        delete_query = delete(Users).where(Users.id == ident)
        await db.execute(delete_query)
        await db.commit()
    else:
        raise HTTPException(status_code=403, detail="Bu amalni bajarishga ruxsat yo'q!")


async def logout_user(db: AsyncSession, user):
    await db.execute(delete(Users).where(Users.id == user.id))
    await db.commit()