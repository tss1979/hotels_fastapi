from fastapi import HTTPException

class HotelAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__( self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelAppException):
    detail = "Сущность не найдена"

class ObjectAlreadyExistsException(HotelAppException):
    detail = "Объект уже существует"

class  AllRoomsAreBooked(HotelAppException):
    detail = "Не осталось номеров выбранной категории"


def check_date_to_is_after_date_from(date_from, date_to):
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть раньше даты выезда")