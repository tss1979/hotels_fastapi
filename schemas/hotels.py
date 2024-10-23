from pydantic import BaseModel

class Hotel(BaseModel):
    name: str
    rooms: int

class HotelPATCH(BaseModel):
    name:  str | None = None
    rooms: int | None = None
