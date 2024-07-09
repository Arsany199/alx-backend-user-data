#!/usr/bin/env python3
"""model of basic auth."""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """define basic authentication class"""

    def extract_base64_auth_header(self, authorization_header: str) -> str:
        """function extract base64 authorization header """

        if authorization_header is None:
            return (None)

        if not isinstance(authorization_header, str):
            return (None)

        if not authorization_header.startswith("Basic "):
            return (None)

        encoded = authorization_header.split(' ', 1)[1]

        return (encoded)

    def decode_base64_auth_header(self,
                                  base64_authorization_header: str) -> str:
        """dunction decodes the value of a base64 str"""
        if base64_authorization_header is None:
            return (None)
        if not isinstance(base64_authorization_header, str):
            return (None)

        try:
            encoding = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoding)
            decoding = decoded64.decode('utf-8')
        except BaseException:
            return (None)

        return (decoding)

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """function returns the user email and password"""

        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)

        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """function return the user instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return (None)

        if user_pwd is None or not isinstance(user_pwd, str):
            return (None)

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return (None)

        for u in found_users:
            if u.is_valid_password(user_pwd):
                return u

        return (None)

    def current_user(self, request=None) -> TypeVar('User'):
        """function overloads Auth and retrieves the User instance"""
        auth_header = self.authorization_header(request)

        if not auth_header:
            return (None)

        encoding = self.extract_base64_authorization_header(auth_header)

        if not encoding:
            return (None)

        decoding = self.decode_base64_authorization_header(encoding)

        if not decoding:
            return (None)

        email, pwd = self.extract_user_credentials(decoding)

        if not email or not pwd:
            return (None)

        user = self.user_object_from_credentials(email, pwd)

        return (user)
