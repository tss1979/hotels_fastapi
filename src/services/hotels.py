from datetime import date

from src.app.dependencies import PaginationDep
from src.exceptions import check_date_to_is_after_date_from, HotelNotFoundException, ObjectNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_hotels(self,
                         pagination: PaginationDep,
                         location: str | None,
                         title: str | None,
                         date_from: date ,
                         date_to: date
                         ):
        check_date_to_is_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),)

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotels_data: HotelAdd):
        hotel = await self.db.hotels.add(hotels_data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.update(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partial_hotel_update(self, hotel_id: int, hotel_data: HotelPATCH):
        await self.db.hotels.update(hotel_data, id=hotel_id, exclude_unset=True)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
