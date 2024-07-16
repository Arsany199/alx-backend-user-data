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
from sqlalchemy import or_
from user import Base, User


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
        """function that adds a using with email and password"""
        the_user = User(email=email, hashed_password=hashed_password)
        self._session.add(the_user)
        self._session.commit()
        return (the_user)

    def find_user_by(self, **kwargs) -> User:
        """function to find users by a keyword (id, email,...)"""
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return (user)

    def update_user(self, user_id: int, **kwargs) -> None:
        """function use find_user_by to locate user then update it"""
        user = self.find_user_by(id=user_id)

        for k, _ in kwargs.items():
            if not hasattr(user, k):
                raise ValueError("invalid argument {}".format(k))

        for k, v in kwargs.items():
            setattr(user, k, v)

        self._session.commit()
