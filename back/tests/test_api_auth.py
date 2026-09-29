import os
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from taximetro import api
from taximetro.api import app, get_session
from taximetro.ride_session import RideSession
from taximetro.infrastructure.storage.db_storage import DbStorage


class TestApiAuth(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.auth_path = os.path.join(self.tmp_dir, "auth.ini")
        patcher = patch.object(api, "AUTH_PATH", self.auth_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        api._tokens.clear()
        session = RideSession({"stopped_rate": 0.02, "moving_rate": 0.05}, DbStorage(os.path.join(self.tmp_dir, "t.db")))
        app.dependency_overrides[get_session] = lambda: session
        self.addCleanup(app.dependency_overrides.clear)
        self.client = TestClient(app)

    def _setup_password(self, password="secreto123"):
        return self.client.post("/api/auth/setup", json={"password": password})

    def test_status_reports_no_password_on_fresh_install(self):
        self.assertEqual(self.client.get("/api/auth/status").json(), {"password_set": False})

    def test_setup_sets_password_and_returns_working_token(self):
        response = self._setup_password()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.client.get("/api/auth/status").json()["password_set"])
        headers = {"Authorization": f"Bearer {response.json()['token']}"}
        self.assertEqual(self.client.get("/api/ride", headers=headers).status_code, 404)  # authed, just no ride

    def test_setup_twice_returns_409(self):
        self._setup_password()
        self.assertEqual(self._setup_password("otra").status_code, 409)

    def test_setup_rejects_blank_password(self):
        self.assertEqual(self._setup_password("   ").status_code, 422)

    def test_login_wrong_password_returns_401(self):
        self._setup_password()
        response = self.client.post("/api/auth/login", json={"password": "incorrecta"})
        self.assertEqual(response.status_code, 401)

    def test_login_correct_password_returns_token(self):
        self._setup_password()
        response = self.client.post("/api/auth/login", json={"password": "secreto123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_without_password_set_returns_401(self):
        response = self.client.post("/api/auth/login", json={"password": "x"})
        self.assertEqual(response.status_code, 401)

    def test_protected_routes_reject_missing_or_bad_token(self):
        self.assertEqual(self.client.get("/api/rides").status_code, 401)
        self.assertEqual(self.client.get("/api/rides", headers={"Authorization": "Bearer nope"}).status_code, 401)


if __name__ == "__main__":
    unittest.main()
