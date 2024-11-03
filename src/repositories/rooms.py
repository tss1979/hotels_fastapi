from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm

    async def get_all(
            self,
            hotel_id,
    ):
        query = select(self.model)
        if hotel_id:
            query = query.filter(hotel_id=hotel_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Room.model_validate(model, from_attributes=True) for model in result.scalars().all()]