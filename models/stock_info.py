from __future__ import annotations
from typing import Union, Dict, List
from datetime import datetime

from stock_api import FinMind

from models import DatabaseManager, db


class StockInfo(db.Model):    # type: ignore
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'stock_info'

    _id = db.Column(db.Integer, primary_key=True)
    _stock_id = db.Column(db.String, nullable=False, unique=True)
    _stock_name = db.Column(db.String, nullable=False, unique=False)
    _industry = db.Column(db.String, nullable=False, unique=False)
    _type = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, stock_id: str, stock_name: str, industry: str, type: str) -> None:
        self._stock_id = stock_id
        self._stock_name = stock_name
        self._industry = industry
        self._type = type

    def __repr__(self) -> str:
        return '<StockInfo[{id}]: {stock_id} {short_name}>'.format(
            id=self.id, stock_id=self.stock_id, short_name=self.stock_name
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
    def stock_name(self) -> str:
        return self._stock_name

    @stock_name.setter
    def stock_name(self, value: str) -> str:
        self._stock_name = value
        DatabaseManager.update()
        return self.stock_name

    @property
    def industry(self) -> str:
        return self._industry

    @industry.setter
    def industry(self, value: str) -> str:
        self._industry = value
        DatabaseManager.update()
        return self.industry

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> str:
        self._type = value
        DatabaseManager.update()
        return self.type

    @classmethod
    def create(cls, stock_id: str, stock_name: str, industry: str, type: str) -> StockInfo:
        stock_info: StockInfo = cls(stock_id, stock_name, industry, type)
        if not DatabaseManager.create(stock_info):
            raise RuntimeError
        return stock_info

    @classmethod
    def upgrade(cls) -> bool:
        from models import DataUpdateHistory

        history: Union[DataUpdateHistory, None] = DataUpdateHistory.query.filter_by(_table=cls.__tablename__).first()
        if history != None and not history.is_expired(days=7):
            return False

        stock_info: List[Dict[str, str]] = FinMind.stock_info()
        cls.clean()

        for entry in stock_info:
            cls.create(
                stock_id=entry['stock_id'],
                stock_name=entry['stock_name'],
                industry=entry['industry_category'],
                type=entry['type']
            )

        if history != None:
            history.datetime = datetime.now()
        else:
            history = DataUpdateHistory.create(table=cls.__tablename__, datetime=datetime.now())

        return True

    @classmethod
    def get_name(cls, stock_id: str) -> Union[str, None]:
        try:
            stock_info: StockInfo = cls.query.filter_by(_stock_id=stock_id).first()
            return stock_info.stock_name
        except:
            return None

    @classmethod
    def get_id(cls, stock_name: str) -> Union[str, None]:
        try:
            stock_info: StockInfo = cls.query.filter_by(_stock_name=stock_name).first()
            return stock_info.stock_id
        except:
            return None

    @classmethod
    def clean(cls) -> bool:
        cls.query.delete()
        return DatabaseManager.update()
