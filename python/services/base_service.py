from services.database import get_connection


class BaseService:
    def __init__(self):
        self.conn = get_connection()

    def close(self):
        self.conn.close()
