from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_database
from functions.gamification import get_student_gamification, get_leaderboard
from schemas.gamification import GamificationProfile, LeaderboardEntry
from routes.auth import get_current_active_user
from schemas.users import CreateUser

gamification_router = APIRouter(
    prefix="/api/gamification",
    tags=["Gamification"]
)


@gamification_router.get('/leaderboard', response_model=List[LeaderboardEntry])
async def reyting(limit: int = 10, group_id: int = None,
                  db: AsyncSession = Depends(get_database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_leaderboard(limit, group_id, db, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))


@gamification_router.get('/students/{student_id}', response_model=GamificationProfile)
async def oquvchi_gamifikatsiyasi(student_id: int,
                                  db: AsyncSession = Depends(get_database),
                                  current_user: CreateUser = Depends(get_current_active_user)):
    try:
        return await get_student_gamification(student_id, db, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))
