from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserAdd, UserRequestAdd
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def check_email(self, data: UserRequestAdd):
        query = select(self.model).filter_by(email=data.email)
        return await self.session.execute(query).scalars().one_or_none()