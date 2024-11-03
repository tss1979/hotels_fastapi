from pydantic import BaseModel

class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

class RoomPATCH(BaseModel):
    title: str | None
    description: str | None
    price: int | None
    quantity: int | None

