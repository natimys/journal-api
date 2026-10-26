from pydantic import BaseModel


class Group(BaseModel):
    group_status: int
    is_primary: bool
    id: int
    name: str

class TopCoins(BaseModel):
    points: int

class TopGems(BaseModel):
    points: int

class GamingPoints(BaseModel):
    coins: TopCoins
    gems: TopGems

class UserInfo(BaseModel):
    full_name: str
    birth_date: str
    groups: list[Group]
    student_id: int
    stream_id: int
    level: int
    photo: str | None = None
    gaming_points: GamingPoints
