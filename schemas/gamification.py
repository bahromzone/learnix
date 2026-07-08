from typing import List, Optional
from pydantic import BaseModel


class Badge(BaseModel):
    code: str
    name: str
    description: str


class GamificationProfile(BaseModel):
    student_id: int
    full_name: str
    points: int
    level: int
    level_name: str
    next_level_at: Optional[int] = None
    points_to_next_level: Optional[int] = None
    present_count: int
    total_sessions: int
    attendance_rate: float
    badges: List[Badge]


class LeaderboardEntry(GamificationProfile):
    rank: int
