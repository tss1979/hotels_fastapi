from contextlib import asynccontextmanager
import sys
from pathlib import Path

import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from init import redis_manager
from src.app.facilities import router_facilities
from src.app.hotels import router_hotels
from src.app.auth import router_auth
from src.app.rooms import router_rooms
from src.app.bookings import router_bookings
from src.app.images import router_images
from src.config import settings

sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()

# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
