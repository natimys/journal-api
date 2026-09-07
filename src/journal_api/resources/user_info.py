from models.user_info import GamingPoints, Group, UserInfo

from .base import Base


class UserInfoResource(Base):
    async def get(self):
        response = await self.client.get("/settings/user-info")
        response_json = await response.json()
        return UserInfo(
            full_name=response_json.get("full_name"),
            birth_date=response_json.get("birthday"),
            groups=[Group(**response_json.get("groups"))],
            student_id=response_json.get("student"),
            stream_id=response_json.get("stream_id"),
            level=response_json.get("level"),
            photo=response_json.get("photo"),
            gaming_points=GamingPoints(
                coins=response_json.get("gaming_points")[0],
                gems=response_json.get("gaming_points")[1],
            ),
        )
