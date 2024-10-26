from src.app.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH
from fastapi import APIRouter

hotels = [
    {"id": 1, "name": "Sochi", "rooms": 100},
    {"id": 2, "name": "Дубай", "rooms": 500},
    {"id": 3, "name": "Мальдивы", "rooms": 120},
    {"id": 4, "name": "Геленджик", "rooms": 50},
    {"id": 5, "name": "Москва", "rooms": 200},
    {"id": 6, "name": "Казань", "rooms": 80},
    {"id": 7, "name": "Санкт-Петербург", "rooms": 120},
]

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])

@router_hotels.get("/", summary="Получение полного списка отелей")
def get_hotels(pagination: PaginationDep):
    start = (pagination.page - 1) * pagination.per_page
    finish = start + pagination.per_page
    return hotels[start:finish]

@router_hotels.delete("/{hotel_id}", summary="Удаление отеля по идентификатору")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}

@router_hotels.post("/", summary="Добавление нового отеля")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "name": hotel_data.name, "rooms": hotel_data.rooms})
    return {"status": "Ok"}

@router_hotels.put("/{hotel_id}", summary="Изменение данных отеля")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["name"] = hotel_data.name
    hotel["rooms"] = hotel_data.rooms
    return {"status": "Ok"}

@router_hotels.patch("/{hotel_id}", summary="Частичное изменение данных отеля")
def partial_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.name is not None:
        hotel["name"] = hotel_data.name
    if hotel_data.rooms is not None:
        hotel["rooms"] = hotel_data.rooms
    return {"status": "Ok"}