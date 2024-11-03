from datetime import date
from pydantic import BaseModel

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(BaseModel):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int

class BookingPATCH(BaseModel):
    room_id: int | None = None
    user_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None