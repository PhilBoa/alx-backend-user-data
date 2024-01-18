#!/usr/bin/env python3
"""
Basic authentication module
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class for API authentication
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header for Basic
        Authentication
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        # Check if the header starts with 'Basic ' and has at least one
        # character after the space
        if not authorization_header.startswith('Basic '):
            return None

        # Extract the Base64 part after 'Basic '
        base64_part = authorization_header.split(' ')[1]

        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes the value of a Base64 string
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string and return as UTF-8
            decoded_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            # Return None for invalid Base64
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        # Check if the decoded string contains ':'
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Use regex to extract user email and password
        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        match = re.fullmatch(
                pattern, decoded_base64_authorization_header.strip())

        if match:
            user_email = match.group('user')
            user_password = match.group('password')
            return user_email, user_password

        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the database based on email
        users = User.search({'email': user_email})

        # If no user found with the given email, return None
        if not users:
            return None

        user = users[0]
        if user.is_valid_password(user_pwd):
            return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        # Extract Authorization header from the request
        auth_header = self.authorization_header(request)

        # Extract Base64 part of the Authorization header
        base64_header = self.extract_base64_authorization_header(auth_header)

        # Decode Base64 Authorization header
        decoded_header = self.decode_base64_authorization_header(base64_header)

        # Extract user credentials from the decoded header
        user_email, user_pwd = self.extract_user_credentials(decoded_header)

        return self.user_object_from_credentials(user_email, user_pwd)
