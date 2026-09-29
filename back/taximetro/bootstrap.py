"""Composition root: the only place that picks concrete classes for the ports."""
from taximetro import settings
from taximetro.application.auth_service import AuthService
from taximetro.application.ride_service import RideService
from taximetro.application.token_store import TokenStore
from taximetro.infrastructure.ini_account_repository import IniAccountRepository
from taximetro.infrastructure.ini_rates_repository import IniRatesRepository
from taximetro.infrastructure.pbkdf2_password_hasher import Pbkdf2PasswordHasher
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository


def build_ride_service():
    return RideService(IniRatesRepository(settings.RATES_PATH), SqliteRideRepository(settings.DB_PATH))


def build_auth_service():
    return AuthService(IniAccountRepository(settings.AUTH_PATH), Pbkdf2PasswordHasher(), TokenStore())
