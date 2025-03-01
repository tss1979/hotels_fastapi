from datetime import date
from fastapi import HTTPException
from src.exceptions import check_date_to_is_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException
from src.app.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd
from fastapi import APIRouter, Body, Query

from src.services.hotels import HotelService

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])


@router_hotels.get("/", summary="Получение полного списка отелей")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Расположение отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-08-12"),
    date_to: date = Query(example="2024-08-16"),
):
    return await HotelService(db).get_hotels(pagination, location, title, date_from, date_to)


@router_hotels.get("/{hotel_id}", summary="Получение отеля по идентификатору")
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router_hotels.post("/create", summary="Добавление отеля")
async def create_hotel(
    db: DBDep,
    hotels_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Хаятт",
                "value": {
                    "title": "Hyatt",
                    "location": "Москва, ул. Неглинная, 4",
                },
            },
            "2": {
                "summary": "Ритц",
                "value": {
                    "title": "Ritz",
                    "location": "Москва, ул. Тверская, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotels_data)
    return {"status": "OK", "data": hotel}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля по идентификатору")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "Ok"}


@router_hotels.put("/{hotel_id}", summary="Изменение данных отеля")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "Ok"}


@router_hotels.patch("/{hotel_id}", summary="Частичное изменение данных отеля")
async def partial_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    try:
        await HotelService(db).partial_hotel_update(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "Ok"}
