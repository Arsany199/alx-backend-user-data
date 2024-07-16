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


def _generate_uuid() -> str:
    """function to generate uuid"""
    return str(uuid.uuid4())
