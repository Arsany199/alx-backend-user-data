#!/usr/bin/env python3
"""model for session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """defines session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """function that creates a session ID for a user_id"""

        if user_id is None or not isinstance(user_id, str):
            return (None)

        sess_id = str(uuid.uuid4())

        self.user_id_by_session_id[sess_id] = user_id

        return (sess_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """function that returns user ID based on a session ID"""

        if session_id is None or not isinstance(session_id, str):
            return (None)

        return (self.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        """function that returns a user instance based on a cookie value"""

        sess_id = self.session_cookie(request)

        if sess_id is None:
            return (None)

        user_id = self.user_id_for_session_id(sess_id)

        return (User.get(user_id))

    def destroy_session(self, request=None):
        """function that removes user session / logout"""

        if request is None:
            return (False)

        sess_id = self.session_cookie(request)
        if sess_id is None:
            return (False)

        user_id = self.user_id_for_session_id(sess_id)

        if not user_id:
            return (False)

        try:
            del self.user_id_by_session_id[sess_id]
        except Exception:
            pass

        return (True)
