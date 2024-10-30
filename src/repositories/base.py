from sqlalchemy import select, insert

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

    async def add(self, **data):
        add_stmt = insert(self.model).values(**data.model_dump())
        id = await self.session.execute(add_stmt)
        return self.session.query(HotelsOrm).get(id)
