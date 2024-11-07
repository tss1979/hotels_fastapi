from src.app.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from fastapi import APIRouter, Body

router_facilities = APIRouter(prefix="/facilities", tags=["Услуги"])

@router_facilities.get("/")
async def get_all(db: DBDep):
    return await db.facilities.get_all_filtered()

@router_facilities.post("/create")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body(openapi_examples={
    "1": {
        "summary": "Интернет",
        "value": {
            "title": "Интернет",
        }
    },
    "2": {
        "summary": "Пляж",
        "value": {
            "title": "Пляж",
        },

    }
})):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}

