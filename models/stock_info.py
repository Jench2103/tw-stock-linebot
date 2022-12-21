from __future__ import annotations
from typing import Union, Dict, List
from datetime import datetime

from stock_api import TWSE

from models import DatabaseManager, db


class StockInfo(db.Model):    # type: ignore
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'stock_info'

    _id = db.Column(db.Integer, primary_key=True)
    _stock_id = db.Column(db.String, nullable=False, unique=True)
    _short_name = db.Column(db.String, nullable=False, unique=True)
    _full_name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, stock_id: str, short_name: str, full_name: str) -> None:
        self._stock_id = stock_id
        self._short_name = short_name
        self._full_name = full_name

    def __repr__(self) -> str:
        return '<StockInfo[{id}]: {stock_id} {short_name}>'.format(
            id=self.id, stock_id=self.stock_id, short_name=self.short_name
        )

    @property
    def id(self) -> int:
        return self._id

    @property
    def stock_id(self) -> str:
        return self._stock_id

    @stock_id.setter
    def stock_id(self, value: str) -> str:
        self._stock_id = value
        DatabaseManager.update()
        return self.stock_id

    @property
    def short_name(self) -> str:
        return self._short_name

    @short_name.setter
    def short_name(self, value: str) -> str:
        self._short_name = value
        DatabaseManager.update()
        return self.short_name

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> str:
        self._full_name = value
        DatabaseManager.update()
        return self.full_name

    @classmethod
    def create(cls, stock_id: str, short_name: str, full_name: str) -> StockInfo:
        stock_info: StockInfo = cls(stock_id, short_name, full_name)
        if not DatabaseManager.create(stock_info):
            raise RuntimeError
        return stock_info

    @classmethod
    def upgrade(cls) -> bool:
        from models import DataUpdateHistory

        history: Union[DataUpdateHistory, None] = DataUpdateHistory.query.filter_by(_table=cls.__tablename__).first()
        if history != None and not history.is_expired(days=7):
            return False

        twse_stock_info: List[Dict[str, str]] = TWSE.OpenData.get_listed_company()
        cls.clean()

        for entry in twse_stock_info:
            cls.create(stock_id=entry['公司代號'], short_name=entry['公司簡稱'], full_name=entry['公司名稱'])

        if history != None:
            history.datetime = datetime.now()
        else:
            history = DataUpdateHistory.create(table=cls.__tablename__, datetime=datetime.now())

        return True

    @classmethod
    def get_name(cls, stock_id: str) -> Union[str, None]:
        try:
            stock_info: StockInfo = cls.query.filter_by(_stock_id=stock_id).first()
            return stock_info.short_name
        except:
            return None

    @classmethod
    def get_id(cls, short_name: str) -> Union[str, None]:
        try:
            stock_info: StockInfo = cls.query.filter_by(_short_name=short_name).first()
            return stock_info.stock_id
        except:
            return None

    @classmethod
    def clean(cls) -> bool:
        cls.query.delete()
        return DatabaseManager.update()
