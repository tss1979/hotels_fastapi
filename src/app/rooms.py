from src.app.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest, RoomPATCHRequest
from fastapi import APIRouter, Body

router_rooms = APIRouter(prefix="/hotels", tags=["Номера"])


@router_rooms.get("/{hotel_id}/rooms", summary="Получение полного списка номеров")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_all(hotel_id=hotel_id)

@router_rooms.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по идентификатору")
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router_rooms.post("/{hotel_id}/rooms/create", summary="Добавление номера")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Стандарт",
        "value": {
            "title": "Стандарт",
            "description": "30 m2",
            "price": 15000,
            "quantity": 100,
        }
    },
    "2": {
        "summary": "Президенский люкс",
        "value": {
            "title": "Президенский люкс",
            "description": "130 m2",
            "price": 150000,
            "quantity": 1,
        }
    }
})):

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router_rooms.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по идентификатору")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Ok"}


@router_rooms.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных номера")
async def edit_hotel(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "Ok"}

@router_rooms.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера")
async def partial_edit_hotel(hotel_id: int, room_id: int, room_data: RoomPATCHRequest, db: DBDep):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "Ok"}