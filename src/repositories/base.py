from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from src.models.hotels import HotelsOrm


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self,  *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def delete(self, hotel_id: int) -> None:
        query = delete(self.model).where(id=hotel_id)
        await self.session.execute(query)

    async def update(self, data: BaseModel):
        update_stmt = (update(self.model).
                       where(id=data.id).
                       values(**data.model_dump()))
        await self.session.execute(update_stmt)




