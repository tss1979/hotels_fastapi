from datetime import date

from src.schemas.bookings import BookingAdd


async def test_crud_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all(hotel_id=1))[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2019, month=12, day=12),
        date_to=date(year=2020, month=1, day=1),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id

    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2019, month=12, day=12),
        date_to=date(year=2020, month=1, day=1),
        price=5000,
    )

    await db.bookings.update(update_booking_data, id=new_booking.id)
    edited_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert edited_booking
    assert edited_booking.id == new_booking.id
    assert edited_booking.price == 5000

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking




