
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int |  None, Query(1, ge=1)]
    per_page: Annotated[int| None, Query(None, ge=1, lt=30)]

def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data.get("id", None)


PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[int, Depends(get_current_user_id)]
