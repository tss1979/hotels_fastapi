from src.app.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from fastapi import APIRouter, HTTPException

router_bookings = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router_bookings.post("/create", summary="Добавление бронирования")
async def booking_create(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router_bookings.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router_bookings.get("/me", summary="Получение бронирований текущего пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_all_filtered(user_id=user_id)
