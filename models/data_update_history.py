from __future__ import annotations

from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta

from models import DatabaseManager, db


class DataUpdateHistory(db.Model):    # type: ignore
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'data_update_history'

    _id = db.Column(db.Integer, primary_key=True)
    _table = db.Column(db.String, nullable=False, unique=True)
    _datetime = db.Column(db.DateTime, nullable=True, unique=False)

    def __init__(self, table: str, datetime: DateTime = DateTime.now()) -> None:
        self._table = table
        self._datetime = datetime

    @property
    def id(self) -> int:
        return self._id

    @property
    def table(self) -> str:
        return self._table

    @table.setter
    def table(self, value: str) -> str:
        self._table = value
        DatabaseManager.update()
        return self.table

    @property
    def datetime(self) -> DateTime:
        return self._datetime

    @datetime.setter
    def datetime(self, value: DateTime = DateTime.now()) -> DateTime:
        self._datetime = value
        DatabaseManager.update()
        return self.datetime

    def is_expired(self, days: int) -> bool:
        return DateTime.now() - self.datetime > TimeDelta(days=days)

    @classmethod
    def create(cls, table: str, datetime: DateTime = DateTime.now()) -> DataUpdateHistory:
        data_update_history: DataUpdateHistory = cls(table=table, datetime=datetime)
        if not DatabaseManager.create(data_update_history):
            raise RuntimeError
        return data_update_history
