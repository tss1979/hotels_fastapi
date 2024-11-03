
from src.app.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from fastapi import APIRouter, HTTPException

router_bookings = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router_bookings.post("/create", summary="Добавление бронирования")
async def booking_create(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    data = booking_data.model_dump()
    room = await db.rooms.get_one_or_none(id=data["room_id"])
    if not room:
        raise HTTPException(status_code=404, detail="Выбранный номер не существует")
    print(user_id, room.model_dump()["price"])
    print(data)
    _booking_data = BookingAdd(user_id=user_id, price=room.model_dump()["price"], **data)
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "booking": booking}