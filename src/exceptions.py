

class HotelAppException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__( self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelAppException):
    detail = "Сущность не найдена"
