import unittest
import os
from fastapi.testclient import TestClient
from taximetro.api import app, get_session
from taximetro.ride_session import RideSession
from taximetro.infrastructure.storage.db_storage import DbStorage

class TestApi(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_api.db"
        rates = {"stopped_rate": 0.02, "moving_rate": 0.05}
        self.session = RideSession(rates, DbStorage(self.test_db))
        app.dependency_overrides[get_session] = lambda: self.session
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_start_state_end_happy_path(self):
        start_response = self.client.post("/api/ride/start")
        self.assertEqual(start_response.status_code, 201)
        self.assertEqual(start_response.json()["state"], "stopped")

        state_response = self.client.patch("/api/ride/state", json={"state": "moving"})
        self.assertEqual(state_response.status_code, 200)
        self.assertEqual(state_response.json()["state"], "moving")

        end_response = self.client.post("/api/ride/end")
        self.assertEqual(end_response.status_code, 200)
        body = end_response.json()
        self.assertIn("id", body)
        self.assertAlmostEqual(body["amount"], self.session.storage.load_today()[0].accumulated)

    def test_start_twice_returns_409(self):
        self.client.post("/api/ride/start")
        response = self.client.post("/api/ride/start")
        self.assertEqual(response.status_code, 409)

    def test_state_without_active_ride_returns_404(self):
        response = self.client.patch("/api/ride/state", json={"state": "moving"})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
