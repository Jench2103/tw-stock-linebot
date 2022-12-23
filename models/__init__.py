import flask_sqlalchemy

from flask_line import db


class DatabaseManager():
    @staticmethod
    def create(object: flask_sqlalchemy.Model) -> bool:
        if not isinstance(object, flask_sqlalchemy.Model):
            return False
        db.session.add(object)
        return DatabaseManager.update()

    @staticmethod
    def update() -> bool:
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete(object: flask_sqlalchemy.Model) -> bool:
        if not isinstance(object, flask_sqlalchemy.Model):
            return False
        db.session.delete(object)
        return DatabaseManager.update()


from .stock_info import StockInfo
from .data_update_history import DataUpdateHistory
from .user_stock import UserStock
