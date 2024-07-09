#!/usr/bin/env python3
"""model for authentication"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """defines authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """function to check if auth is required"""
        if path is None:
            return (True)

        if excluded_paths is None or not excluded_paths:
            return (True)

        for i in excluded_paths:
            if fnmatch.fnmatch(path, i):
                return (False)

        return (True)

    def authorization_header(self, request=None) -> str:
        """function to get authorization header"""
        if request is None:
            return (None)
        return (request.headers.get('Authorization', None))

    def current_user(self, request=None) -> TypeVar('User'):
        """function to get user from request"""
        return (None)
