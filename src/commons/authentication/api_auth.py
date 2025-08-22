"""API authentication module."""

import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from commons.authentication.models import CurrentUser


class ApiAuth:
    """A class to handle API authentication."""

    def __init__(self, auth_url: str):
        """Initializes the ApiAuth with the provided authentication URL.

        Args:
            auth_url: The authentication URL.
        """
        self.auth_url = auth_url

    def authenticate(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> CurrentUser:
        """Authenticate the API request using the provided token.

        Args:
            token: The authentication token.

        Returns:
            CurrentUser: The authenticated user information.

        Raises:
            HTTPException: If authentication fails or the token is invalid.
        """
        token = credentials.credentials
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(
                self.auth_url,
                headers=headers,
                timeout=30,
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Authentication failed: {response.text}",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {str(e)}",
            ) from e
        return CurrentUser(**response.json().get("user"))
