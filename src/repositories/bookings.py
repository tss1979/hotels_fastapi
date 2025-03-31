from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking, BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def add_booking(self, data: BookingAdd, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id)
        rooms_ids_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids = rooms_ids_res.scalars().all()
        if data.room_id in rooms_ids:
            new_booking = await self.add(data)
            return new_booking



