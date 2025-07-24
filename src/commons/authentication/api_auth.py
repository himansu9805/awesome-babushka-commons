"""API authentication module."""

import requests


class ApiAuth:
    """A class to handle API authentication."""

    def __init__(self, auth_url: str, disable_auth: bool = False):
        """Initializes the ApiAuth with the provided authentication URL.

        Args:
            auth_url: The authentication URL.
            disable_auth: Flag to disable authentication.
        """
        self.auth_url = auth_url
        self.disable_auth = disable_auth

    def authenticate(self, token: str) -> bool:
        """Authenticate the API request using the provided token.

        Args:
            token: The authentication token.

        Returns:
            bool: True if authenticated, False otherwise.
        """
        if self.disable_auth:
            return True

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            self.auth_url,
            headers=headers,
            timeout=30,
        )
        if response.status_code != 200:
            return False
        return True
