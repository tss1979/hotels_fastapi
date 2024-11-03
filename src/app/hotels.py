from src.app.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from fastapi import APIRouter, Body, Query

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])


@router_hotels.get("/", summary="Получение полного списка отелей")
async def get_hotels(pagination: PaginationDep,
                     location: str | None = Query(None, description="Расположение отеля"),
                     title: str | None = Query(None, description="Название отеля"),
                     ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1))

@router_hotels.get("/{hotel_id}", summary="Получение отеля по идентификатору")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)

@router_hotels.post("/create", summary="Добавление отеля")
async def create_hotel(hotels_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Хаятт",
        "value": {
            "title": "Hyatt",
            "location": "Москва, ул. Неглинная, 4",
        }
    },
    "2": {
        "summary": "Ритц",
        "value": {
            "title": "Ritz",
            "location": "Москва, ул. Тверская, 2",
        }
    }
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotels_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router_hotels.delete("/{hotel_id}", summary="Удаление отеля по идентификатору")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "Ok"}


@router_hotels.put("/{hotel_id}", summary="Изменение данных отеля")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "Ok"}

@router_hotels.patch("/{hotel_id}", summary="Частичное изменение данных отеля")
async def partial_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "Ok"}

