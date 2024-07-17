#!/usr/bin/env python3
"""model to encrypt password"""
import logging
from typing import Union
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """function that encrypt the password"""
    encoding = password.encode()
    hashing = bcrypt.hashpw(encoding, bcrypt.gensalt())

    return (hashing)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """function that regester users"""
        try:
            self._db.find_user_by(email=email)
            # if the user exists raise
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return (user)

    def valid_login(self, email: str, password: str) -> bool:
        """function to check for the valid email and password"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                # Check the password matching
                encrypt = password.encode()
                if bcrypt.checkpw(encrypt, user.hashed_password):
                    return (True)
        except NoResultFound:
            return (False)
        return (False)

    def create_session(self, email: str) -> str:
        """function that find user corresponding to email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """function returns the corresponding user using session id"""
        if session_id is None:
            return (None)

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return (None)
        return (user)

    def destroy_session(self, user_id: int) -> None:
        """method finds the corresponding user id and update it to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return (None)
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """find the user using email the reset his token"""
        try:
            myuser = self._db.find_user_by(email=email)
        except NoResultFound:
            myuser = None
        if myuser is None:
            raise ValueError()

        reset_token = _generate_uuid()
        self._db.update_user(myuser.id, reset_token=reset_token)
        return (reset_token)

    def update_password(self, reset_token: str, password: str) -> None:
        """method that find user using reset_token
        then updates the password to None"""
        try:
            myuser = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("not the right token")

        new_pass = _hash_password(password)
        self._db.update_user(myuser.id, hashed_password=new_pass,
                             reset_token=None)


def _generate_uuid() -> str:
    """function to generate uuid"""
    return str(uuid.uuid4())
