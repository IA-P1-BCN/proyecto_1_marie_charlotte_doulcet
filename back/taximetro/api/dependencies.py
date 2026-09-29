from functools import lru_cache
from typing import Annotated
from fastapi import Depends, Header, HTTPException
from taximetro import bootstrap
from taximetro.application.auth_service import AuthService
from taximetro.application.ride_service import RideService


@lru_cache
def get_ride_service() -> RideService:
    """One RideService per process: it holds the single ride in progress."""
    return bootstrap.build_ride_service()


@lru_cache
def get_auth_service() -> AuthService:
    """One AuthService per process: its TokenStore holds the session tokens."""
    return bootstrap.build_auth_service()


RideServiceDep = Annotated[RideService, Depends(get_ride_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def require_auth(auth: AuthServiceDep, authorization: Annotated[str, Header()] = "") -> None:
    if not auth.is_valid_token(authorization.removeprefix("Bearer ")):
        raise HTTPException(status_code=401, detail="Not authenticated")
