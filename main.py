from http.client import HTTPException
from typing import Union

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI(docs_url=None)

class Hotel:
    name: str
    country: str
    city: str
    rooms_total: int
    min_room_price: float
    max_room_price: float

    def __init__(self, name, country, city, rooms_total, min_room_price, max_room_price):
        self.name = name
        self.country = country
        self.city = city
        self.rooms_total = rooms_total
        self.min_room_price = min_room_price
        self.max_room_price = max_room_price

    def __str__(self):
        return f'{self.name} - {self.city}'

hotel_1 = Hotel("Звезда", "Россия", "Москва", 100, 2000, 10000)
hotel_2 = Hotel("Хаятт", "Россия", "Москва", 200, 40000, 400000)
hotel_3 = Hotel("Хаятт", "США", "Сан-Франциско", 500, 40000, 400000)
hotel_4 = Hotel("Люкс", "Россия", "Сочи", 200, 40000, 400000)
hotel_5 = Hotel("Хилтон", "Великобритания", "Лондон", 200, 40000, 400000)

db = {1: hotel_1, 2: hotel_2, 3: hotel_3, 4: hotel_4, 5: hotel_5}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/hotels")
def get_all_hotels():
    global db
    hotels = list(db.values())
    return hotels

@app.put("/hotels/{hotel_id}")
def change_hotel(hotel_id: int, hotel: dict):
    global db
    del db[hotel_id]
    db[hotel_id] = Hotel(**hotel)
    return {"status": "OK"}

@app.patch("/hotels/{hotel_id}")
def change_param(hotel_id: int, param: str, value:  Union[str, int]):
    global db
    hotel = db.get(hotel_id, None).__dict__
    if hotel is not None:
        try:
            hotel[param] = value
            del db[hotel_id]
            db[hotel_id] = Hotel(**hotel)
            return {"status": "OK"}
        except:
            raise HTTPException



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
