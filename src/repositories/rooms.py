from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_rooms_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id)
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rls(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is not None:
            return RoomWithRels.model_validate(model, from_attributes=True)
        else:
            return None

    async def get_all(
        self,
        hotel_id: int,
    ):
        query = select(self.model)
        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [
            Room.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]
