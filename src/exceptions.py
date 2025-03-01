from fastapi import HTTPException

class HotelAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__( self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelAppException):
    detail = "Сущность не найдена"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найдена"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найдена"

class ObjectAlreadyExistsException(HotelAppException):
    detail = "Объект уже существует"

class  AllRoomsAreBooked(HotelAppException):
    detail = "Не осталось номеров выбранной категории"



class HotelAppHTTPException(HTTPException):
    detail = None
    status_code = 500

    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)


class HotelNotFoundHTTPException(HotelAppHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(HotelAppHTTPException):
    status_code = 404
    detail = "Номер не найден"



def check_date_to_is_after_date_from(date_from, date_to):
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть раньше даты выезда")