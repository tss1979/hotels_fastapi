from src.db.db_manager import DBManager


class BaseService:

    def __init__(self, db: DBManager | None):
        self.db = db
