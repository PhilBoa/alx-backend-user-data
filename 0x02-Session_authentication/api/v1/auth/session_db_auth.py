#!/usr/bin/env python3
"""Module defining the SessionDBAuth class for session-based authentication
with database storage."""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ Create and store new instance of UserSession """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return User ID by requesting UserSession in the database based on
        session_id """
        if session_id is None:
            return None

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """ Destroy the UserSession based on the Session ID from the request
        cookie """
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.search({'session_id': session_id})
            if user_session:
                user_session[0].delete()
                return True

        return False
