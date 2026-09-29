import unittest
from fastapi.testclient import TestClient
from taximetro.api import app
from taximetro.api.dependencies import get_auth_service, get_ride_service
from taximetro.application.auth_service import AuthService
from taximetro.application.ride_service import RideService
from taximetro.application.token_store import TokenStore
from taximetro.domain.account import Account
from taximetro.domain.rates import Rates
from tests.fakes import (
    FakePasswordHasher, InMemoryAccountRepository, InMemoryRatesRepository, InMemoryRideRepository,
)


class TestApiAuth(unittest.TestCase):
    def setUp(self):
        self.accounts = InMemoryAccountRepository()
        auth = AuthService(self.accounts, FakePasswordHasher(), TokenStore())
        rides = RideService(InMemoryRatesRepository(Rates(stopped_rate=0.02, moving_rate=0.05)), InMemoryRideRepository())
        app.dependency_overrides[get_auth_service] = lambda: auth
        app.dependency_overrides[get_ride_service] = lambda: rides
        self.addCleanup(app.dependency_overrides.clear)
        self.client = TestClient(app)

    def _register(self, company="Taxis Sol", password="secreto123"):
        return self.client.post("/api/auth/setup", json={"company": company, "password": password})

    def _login(self, company="Taxis Sol", password="secreto123"):
        return self.client.post("/api/auth/login", json={"company": company, "password": password})

    def test_status_reports_not_registered_on_fresh_install(self):
        self.assertEqual(self.client.get("/api/auth/status").json(), {"registered": False})

    def test_setup_registers_company_and_returns_working_token(self):
        response = self._register()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get("/api/auth/status").json(), {"registered": True})
        headers = {"Authorization": f"Bearer {response.json()['token']}"}
        self.assertEqual(self.client.get("/api/ride", headers=headers).status_code, 404)  # authed, just no ride

    def test_setup_twice_returns_409(self):
        self._register()
        self.assertEqual(self._register("Otra", "otra").status_code, 409)

    def test_setup_rejects_blank_company_or_password(self):
        self.assertEqual(self._register("   ", "secreto123").status_code, 422)
        self.assertEqual(self._register("Taxis Sol", "   ").status_code, 422)

    def test_password_from_cli_without_company_counts_as_not_registered(self):
        self.accounts.save(Account(company="", password_hash="fake$vieja"))
        self.assertEqual(self.client.get("/api/auth/status").json(), {"registered": False})
        self.assertEqual(self._register().status_code, 201)
        self.assertEqual(self._login().status_code, 200)  # new password replaced the old one

    def test_login_wrong_password_returns_401(self):
        self._register()
        self.assertEqual(self._login(password="incorrecta").status_code, 401)

    def test_login_wrong_company_returns_401(self):
        self._register()
        self.assertEqual(self._login(company="Otra empresa").status_code, 401)

    def test_login_company_ignores_case_and_outer_spaces(self):
        self._register()
        self.assertEqual(self._login(company="  taxis sol ").status_code, 200)

    def test_login_correct_credentials_returns_token(self):
        self._register()
        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_when_not_registered_returns_401(self):
        self.assertEqual(self._login().status_code, 401)

    def test_protected_routes_reject_missing_or_bad_token(self):
        self.assertEqual(self.client.get("/api/rides").status_code, 401)
        self.assertEqual(self.client.get("/api/rides", headers={"Authorization": "Bearer nope"}).status_code, 401)


if __name__ == "__main__":
    unittest.main()
