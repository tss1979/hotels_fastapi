from datetime import date
from fastapi import HTTPException

from fastapi import APIRouter, Body, Query

from src.app.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest, RoomPATCHRequest
from src.exceptions import check_date_to_is_after_date_from, ObjectNotFoundException

router_rooms = APIRouter(prefix="/hotels", tags=["Номера"])


@router_rooms.get("/{hotel_id}/rooms", summary="Получение полного списка номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    check_date_to_is_after_date_from(date_from, date_to)
    return await db.rooms.get_rooms_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router_rooms.get(
    "/{hotel_id}/rooms/{room_id}", summary="Получение номера по идентификатору"
)
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rls(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=400, detail="Комната не найдена")
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router_rooms.delete(
    "/{hotel_id}/rooms/{room_id}", summary="Удаление номера по идентификатору"
)
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Ok"}


@router_rooms.put("/{hotel_id}/rooms/{room_id}", summary="Изменение данных номера")
async def edit_hotel(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "Ok"}


@router_rooms.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных номера"
)
async def partial_edit_hotel(
    hotel_id: int, room_id: int, room_data: RoomPATCHRequest, db: DBDep
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPATCH(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.update(_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "Ok"}
