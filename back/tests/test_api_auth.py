import os
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from taximetro import api
from taximetro.api import app, get_session
from taximetro.ride_session import RideSession
from taximetro.domain.rates import Rates
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository
from taximetro.infrastructure.auth import hash_password, save_password_hash


class TestApiAuth(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.auth_path = os.path.join(self.tmp_dir, "auth.ini")
        patcher = patch.object(api, "AUTH_PATH", self.auth_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        api._tokens.clear()
        session = RideSession(Rates(stopped_rate=0.02, moving_rate=0.05), SqliteRideRepository(os.path.join(self.tmp_dir, "t.db")))
        app.dependency_overrides[get_session] = lambda: session
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
        save_password_hash(hash_password("vieja"), self.auth_path)
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
