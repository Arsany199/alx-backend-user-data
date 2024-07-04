#!/usr/bin/env python3
"""model to encrypt password"""
import bcrypt


def hash_password(password) -> bytes:
    """function that returns a salted hashed password which is byte string"""
    encoding = password.encode()
    hashing = bcrypt.hashpw(encoding, bcrypt.gensalt())
    return (hashing)
