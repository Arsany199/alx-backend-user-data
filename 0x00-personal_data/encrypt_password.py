#!/usr/bin/env python3
"""model to encrypt password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """function that returns a salted hashed password which is byte string"""
    encoding = password.encode()
    hashing = bcrypt.hashpw(encoding, bcrypt.gensalt())
    return (hashing)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that check if the password matches the hashed password"""
    encoding = password.encode()
    if bcrypt.checkpw(encoding, hashed_password):
        return (True)
    return (False)
