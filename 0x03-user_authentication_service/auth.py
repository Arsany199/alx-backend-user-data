#!/usr/bin/env python3
"""model to encrypt password"""
import logging
from typing import Union
from uuid import uuid4
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
