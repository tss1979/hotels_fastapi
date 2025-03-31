import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient

from src.app.dependencies import get_db
from src.config import settings
from src.db.database import engine_null_pool, async_session_maker_null_pool
from src.db.db_manager import DBManager
from src.models import *
from main import app
from src.schemas.facilities import FacilityAdd
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd



@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)

    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    facility = FacilityAdd.model_validate({"title": "pool"})

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.facilities.add(facility)
        await  db_.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "sobaka@pes.com",
            "password": "111",
        })


@pytest.fixture(scope="session")
async def auth_user(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "sobaka@pes.com",
            "password": "111",
        })
    assert ac.cookies["access_token"]
    yield ac