from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.instructors import get_instructor_profile
from schemas.instructors import InstructorProfile

# Ommaviy (public) router - auth talab qilinmaydi
instructor_router = APIRouter(
    prefix="/instructors",
    tags=["Instructor public profile"]
)


@instructor_router.get('/{ident}', response_model=InstructorProfile)
async def instruktor_profili(ident: int, db: AsyncSession = Depends(get_database)):
    try:
        return await get_instructor_profile(ident, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))
