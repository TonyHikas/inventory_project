from core.db import database


class BaseRepository:

    def __init__(self):
        self.database = database
