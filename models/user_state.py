from __future__ import annotations
from typing import Union

from models import DatabaseManager, db


class UserState(db.Model):    # type: ignore
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user_state'

    _id = db.Column(db.Integer, primary_key=True)
    _userid = db.Column(db.String, nullable=False, unique=True)
    _state = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, userid: str, state: str) -> None:
        self._userid = userid
        self._state = state

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
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str) -> str:
        self._state = value
        DatabaseManager.update()
        return self.state

    @classmethod
    def create(cls, userid: str, state: str) -> UserState:
        user_state: Union[UserState, None] = UserState.query.filter_by(_userid=userid).first()
        if user_state != None:
            return user_state
        else:
            user_state = cls(userid=userid, state=state)
            DatabaseManager.create(user_state)
            return user_state

    @classmethod
    def get_user_state(cls, userid: str) -> Union[str, None]:
        user_state: Union[UserState, None] = UserState.query.filter_by(_userid=userid).first()
        return user_state.state if user_state != None else None

    @classmethod
    def set_user_state(cls, userid: str, state: str) -> None:
        user_state: Union[UserState, None] = UserState.query.filter_by(_userid=userid).first()
        if user_state != None:
            user_state.state = state
        else:
            cls.create(userid=userid, state=state)
