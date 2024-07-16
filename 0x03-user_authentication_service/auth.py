#!/usr/bin/env python3
"""model to encrypt password"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """function that encrypt the password"""
    encoding = password.encode()
    hashing = bcrypt.hashpw(encoding, bcrypt.gensalt())

    return (hashing)
