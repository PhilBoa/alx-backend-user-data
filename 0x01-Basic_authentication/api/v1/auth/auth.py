#!/usr/bin/env python3
""" Authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for a given path
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Make the path slash-tolerant
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                excluded_path = excluded_path[:-1]

            if excluded_path.endswith('*'):
                excluded_path_prefix = excluded_path[:-1]
                if path.startswith(excluded_path_prefix):
                    return False
                elif path.startswith(excluded_path):
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
