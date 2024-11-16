from fastapi_cache.decorator import cache

from init import redis_manager
from src.app.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from fastapi import APIRouter, Body

import json

router_facilities = APIRouter(prefix="/facilities", tags=["Услуги"])

@router_facilities.get("/")
@cache(expire=10)
async def get_all(db: DBDep):
    # facilities_cached = await redis_manager.get("facilities")
    # if not facilities_cached:
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json)
    #     return facilities
    # else:
    #     return json.loads(facilities_cached)
    return await db.facilities.get_all()

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

