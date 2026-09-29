import os
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from taximetro.api import app, get_session, require_auth
from taximetro.domain.rates import Rates
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository
from taximetro.ride_session import RideSession

class TestApi(unittest.TestCase):
    def setUp(self):
        rates = Rates(stopped_rate=0.02, moving_rate=0.05)
        db_path = os.path.join(tempfile.mkdtemp(), "test_api.db")
        self.session = RideSession(rates, SqliteRideRepository(db_path))
        app.dependency_overrides[get_session] = lambda: self.session
        app.dependency_overrides[require_auth] = lambda: None
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

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
        self.assertAlmostEqual(body["amount"], self.session.get_today_history()[0].amount)

    def test_start_twice_returns_409(self):
        self.client.post("/api/ride/start")
        response = self.client.post("/api/ride/start")
        self.assertEqual(response.status_code, 409)

    def test_state_without_active_ride_returns_404(self):
        response = self.client.patch("/api/ride/state", json={"state": "moving"})
        self.assertEqual(response.status_code, 404)

    def test_same_state_returns_409(self):
        self.client.post("/api/ride/start")
        response = self.client.patch("/api/ride/state", json={"state": "stopped"})
        self.assertEqual(response.status_code, 409)

    def test_active_ride_exposes_elapsed_and_current_rate(self):
        self.client.post("/api/ride/start")
        body = self.client.get("/api/ride").json()
        self.assertGreaterEqual(body["elapsed_seconds"], 0)
        self.assertEqual(body["current_rate"], 0.02)

    def test_get_rates(self):
        response = self.client.get("/api/rates")
        self.assertEqual(response.json(), {"stopped_rate": 0.02, "moving_rate": 0.05})

    def test_put_rates_updates_session_and_persists(self):
        with patch("taximetro.ride_session.save_rates") as save:
            response = self.client.put("/api/rates", json={"stopped_rate": 0.03, "moving_rate": 0.06})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.session.rates, Rates(stopped_rate=0.03, moving_rate=0.06))
        self.assertTrue(save.called)

    def test_put_rates_rejects_non_positive(self):
        with patch("taximetro.ride_session.save_rates"):
            response = self.client.put("/api/rates", json={"stopped_rate": 0, "moving_rate": 0.06})
        self.assertEqual(response.status_code, 422)

    def test_start_with_custom_rates_applies_to_that_ride_only(self):
        response = self.client.post("/api/ride/start", json={"stopped_rate": 0.1, "moving_rate": 0.2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["current_rate"], 0.1)
        self.assertEqual(self.session.rates, Rates(stopped_rate=0.02, moving_rate=0.05))

    def test_end_ride_then_history_and_detail_endpoints_return_the_record(self):
        self.client.post("/api/ride/start")
        ended = self.client.post("/api/ride/end").json()

        self.assertEqual(self.client.get("/api/rides").json(), [ended])
        self.assertEqual(self.client.get(f"/api/rides/{ended['id']}").json(), ended)
        self.assertEqual(self.client.get("/api/rides/999").status_code, 404)

    def test_rides_with_an_invalid_date_returns_422(self):
        self.assertEqual(self.client.get("/api/rides?date=not-a-date").status_code, 422)

    def test_start_with_invalid_rates_returns_422(self):
        response = self.client.post("/api/ride/start", json={"stopped_rate": -1, "moving_rate": 0.2})
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
