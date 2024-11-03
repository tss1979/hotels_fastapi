from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH
from fastapi import APIRouter, Body, Query

router_rooms = APIRouter(prefix="/hotels", tags=["Номера"])


@router_rooms.get("{hotel_id}/rooms", summary="Получение полного списка номеров")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)

@router_rooms.get("/{hotel_id}/{room_id}", summary="Получение номера по идентификатору")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)

@router_rooms.post("/{hotel_id}/create", summary="Добавление номера")
async def create_hotel(hotel_id: int, room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Стандарт",
        "value": {
            "title": "Стандарт",
            "hotel_id": 1,
            "description": "30 m2",
            "price": 15000,
            "quantity": 100,
        }
    },
    "2": {
        "summary": "Президенский люкс",
        "value": {
            "title": "Президенский люкс",
            "hotel_id": 1,
            "description": "130 m2",
            "price": 150000,
            "quantity": 1,
        }
    }
})):
    async with async_session_maker() as session:
        room_data["hotel_id"] = hotel_id
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router_rooms.delete("/{hotel_id}/{room_id}", summary="Удаление номера по идентификатору")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=hotel_id)
        await session.commit()
    return {"status": "Ok"}


@router_rooms.put("/{hotel_id}/{room_id}", summary="Изменение данных номера")
async def edit_hotel(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "Ok"}

@router_rooms.patch("/{hotel_id}/{room_id}", summary="Частичное изменение данных номера")
async def partial_edit_hotel(hotel_id: int, room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "Ok"}