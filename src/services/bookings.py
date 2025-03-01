from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):

    async def booking_create(self, user_id: int, booking_data: BookingAddRequest):
        room = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        room_price = room.price
        _booking_data = BookingAdd(
            user_id=user_id, price=room_price, **booking_data.model_dump()
        )
        booking = await self.db.bookings.add(_booking_data)
        await self.db.commit()
        return booking

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_all_filtered(user_id=user_id)