from src.app.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from fastapi import APIRouter, HTTPException

from src.services.bookings import BookingService

router_bookings = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router_bookings.post("/create", summary="Добавление бронирования")
async def booking_create(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:
        booking = await BookingService(db).booking_create(user_id, booking_data)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK", "data": booking}


@router_bookings.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router_bookings.get("/me", summary="Получение бронирований текущего пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)
