#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """

    def __init__(self):
        """ Constructor """
        try:
            duration = int(getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """ Create a session """
        # Create a session using the parent class method
        session_id = super().create_session(user_id)
        if session_id:
            # Update user_id_by_session_id with session dictionary
            session = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            self.user_id_by_session_id[session_id] = session
            return session_id

        return None

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID for session ID """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        user_id = session_dict.get("user_id")
        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
