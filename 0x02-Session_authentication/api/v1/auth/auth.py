#!/usr/bin/env python3
"""
Definition of class Auth
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """defines the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """function that determines whether a given path requires auth"""
        if path is None:
            return (True)
        elif excluded_paths is None or excluded_paths == []:
            return (True)
        elif path in excluded_paths:
            return (False)
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return (False)
                if path.startswith(i):
                    return (False)
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return (False)
        return (True)

    def authorization_header(self, request=None) -> str:
        """function returns the auth header from a request object"""
        if request is None:
            return (None)
        myheader = request.headers.get('Authorization')
        if myheader is None:
            return (None)
        return (header)

    def current_user(self, request=None) -> TypeVar('User'):
        """function that returns user instance from information"""
        return (None)

    def session_cookie(self, request=None):
        """function that return cookies"""
        if request is None:
            return (None)
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
