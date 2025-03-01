from datetime import date
from fastapi import HTTPException

from fastapi import APIRouter, Body, Query

from src.app.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest, RoomPATCHRequest
from src.exceptions import check_date_to_is_after_date_from, ObjectNotFoundException
from src.services.rooms import RoomService

router_rooms = APIRouter(prefix="/hotels", tags=["Номера"])


@router_rooms.get("/{hotel_id}/rooms", summary="Получение полного списка номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_rooms(hotel_id, date_from, date_to)


@router_rooms.get(
    "/{hotel_id}/rooms/{room_id}", summary="Получение номера по идентификатору"
)
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    room = await RoomService(db).get_room_by_id(hotel_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    else:
        return room

@router_rooms.post("/{hotel_id}/rooms/create", summary="Добавление номера")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "title": "Стандарт",
                    "description": "30 m2",
                    "price": 15000,
                    "quantity": 100,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Президенский люкс",
                "value": {
                    "title": "Президенский люкс",
                    "description": "130 m2",
                    "price": 150000,
                    "quantity": 1,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    room = await RoomService(db).create_room(hotel_id, room_data)
    return {"status": "OK", "data": room}


@router_rooms.delete(
    "/{hotel_id}/rooms/{room_id}", summary="Удаление номера по идентификатору"
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "Ok"}


@router_rooms.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных номера")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "Ok"}


@router_rooms.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера"
)
async def partial_edit_hotel(
    hotel_id: int, room_id: int, room_data: RoomPATCHRequest, db: DBDep
):
    await RoomService(db).partial_edit_room(hotel_id, room_id, room_data)
    return {"status": "Ok"}
