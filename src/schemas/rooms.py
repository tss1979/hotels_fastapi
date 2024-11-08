from pydantic import BaseModel

class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int


class RoomPATCHRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None

class RoomPATCH(RoomPATCHRequest):
    hotel_id: int | None = None


