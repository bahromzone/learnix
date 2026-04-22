from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import Base


async def get_in_db(
        db: AsyncSession,
        model,
        ident: int
):

    result = await db.execute(select(model).filter_by(id=ident))
    obj = result.scalars().first()

    if not obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bazada bunday {model} yo'q"
        )
    return obj


async def save_in_db(
        db: AsyncSession,
        obj: Base
):
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj