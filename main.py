
from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI(docs_url=None)



hotels = [{"id": 1, "name": "Hyatt", "rooms": 200}, {"id": 2, "name": "Hilton", "rooms": 200}, {"id": 3, "name": "Lotte", "rooms": 200}, {"id": 4, "name": "Ritz", "rooms": 200}]

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
def get_hotels(
        id: int | None = Query(None, description="Идентификатор"),
        name: str | None = Query(None, description="Название отеля"),
):
    return [hotel for hotel in hotels if hotel["id"] == id and hotel["name"] == name]


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}

@app.post("/hotels")
def create_hotel(name: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "name": name})
    return {"status": "Ok"}

@app.put("/hotels/{hotel_id}")
def edit_hotel(hotel_id: int, name: str = Body(), rooms: str = Body()):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["name"] = name
    hotel["rooms"] = rooms
    return {"status": "Ok"}

@app.patch("/hotels/{hotel_id}")
def edit_hotel(hotel_id: int, name: str | None = Body(None), rooms: str | None= Body(None)):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if name:
        hotel["name"] = name
    if rooms:
        hotel["rooms"] = rooms
    return {"status": "Ok"}





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
