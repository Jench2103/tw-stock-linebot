from __future__ import annotations
from typing import Union, List

from models import DatabaseManager, db


class UserStock(db.Model):    # type: ignore
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user_stock'

    _id = db.Column(db.Integer, primary_key=True)
    _userid = db.Column(db.String, nullable=False, unique=False)
    _stock_id = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, userid: str, stock_id: str) -> None:
        self._userid = userid
        self._stock_id = stock_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def userid(self) -> str:
        return self._userid

    @userid.setter
    def userid(self, value: str) -> str:
        self._userid = value
        DatabaseManager.update()
        return self.userid

    @property
    def stock_id(self) -> str:
        return self._stock_id

    @stock_id.setter
    def stock_id(self, value: str) -> str:
        self._stock_id = value
        DatabaseManager.update()
        return self.stock_id

    def delete(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, userid: str, stock_id: str) -> UserStock:
        user_stock: Union[UserStock, None] = cls.query.filter_by(_userid=userid, _stock_id=stock_id).first()
        if user_stock != None:
            return user_stock
        else:
            user_stock = cls(userid=userid, stock_id=stock_id)
            if not DatabaseManager.create(user_stock):
                raise RuntimeError
            return user_stock

    @classmethod
    def delete_entry(cls, userid: str, stock_id: str) -> bool:
        user_stock: Union[UserStock, None] = cls.query.filter_by(_userid=userid, _stock_id=stock_id).first()
        if user_stock != None:
            return user_stock.delete()
        else:
            return False

    @classmethod
    def get_user_stock(cls, userid: str) -> List[str]:
        result: List[str] = []

        for entry in (cls.query.filter_by(_userid=userid).all() or []):
            entry: UserStock
            result.append(entry.stock_id)

        return sorted(result)

    @classmethod
    def delete_user(cls, userid: str) -> None:
        for entry in (cls.query.filter_by(_userid=userid).all() or []):
            entry: UserStock
            entry.delete()
