#!/usr/bin/env python3
""" Authentication module
"""

from flask import request, current_app
from typing import List, TypeVar


class Auth:
    """ Auth class for API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for a given path
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        elif path in excluded_paths:
            return False

        else:
            for excluded_path in excluded_paths:
                if excluded_path.startswith(path):
                    return False
                if path.startswith(excluded_path):
                    return False
                if excluded_path[-1] == "*":
                    if path.startswith(excluded_path[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Gets the value of the Authorization header from the request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

        if request and 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets the current user based on the request
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Gets the value of the session cookie from the request
        """
        if request is None:
            return None

        session_name = current_app.config.get('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
