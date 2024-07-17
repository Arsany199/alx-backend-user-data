#!/usr/bin/env python3
"""DB module"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add new user to the database with an email and password"""
        the_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(the_user)
            self._session.commit()
        except Exception as err:
            print("Error adding user to database: {}".format(err))
            self._session.rollback()
            raise
        return (the_user)

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """find  users by a specifice attribute"""
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return (user)

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user attribute using id"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found".format(user_id))

        for k, v in kwargs.items():
            if not hasattr(user, k):
                raise ValueError("User has no attribute {}".format(k))
            setattr(user, k, v)

        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError("Invalid request")
