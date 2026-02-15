"""API authentication module."""

import os
import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from commons.authentication.models import CurrentUser

from jose import jwt


class ApiAuth:
    """A class to handle API authentication."""

    def __init__(
        self,
        auth_url: str,
        public_key: str,
        algorithm: str,
        issuer: str,
        audience: str,
    ):
        """Initializes the ApiAuth with the provided authentication URL.

        Args:
            auth_url: The authentication URL.
            public_key: Public key for decoding the token.
            algorithm: Algorithm used to create the token.
            issuer: Name of token issuer.
            audience: Name of audience for which token was issued.
        """
        self.auth_url = auth_url
        self.public_key = public_key
        self.algorithm = algorithm
        self.issuer = issuer
        self.audience = audience

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

        payload = jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm],
            audience=self.audience,
            issuer=self.issuer,
        )

        if payload.get("token_type") != "bearer":
            raise ValueError(
                f"Invalid token type. Expected bearer, "
                f"got {payload.get('token_type')}"
            )

        current_user = CurrentUser(**payload)

        return current_user
