import unittest
from fastapi.testclient import TestClient
from taximetro.api import app
from taximetro.api.dependencies import get_ride_service, require_auth
from taximetro.application.ride_service import RideService
from taximetro.domain.rates import Rates
from tests.fakes import InMemoryRatesRepository, InMemoryRideRepository


class TestApi(unittest.TestCase):
    def setUp(self):
        self.rates_repository = InMemoryRatesRepository(Rates(stopped_rate=0.02, moving_rate=0.05))
        self.session = RideService(self.rates_repository, InMemoryRideRepository())
        app.dependency_overrides[get_ride_service] = lambda: self.session
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
        self.assertAlmostEqual(body["amount"], self.session.get_ride(body["id"]).amount)

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
        response = self.client.put("/api/rates", json={"stopped_rate": 0.03, "moving_rate": 0.06})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"stopped_rate": 0.03, "moving_rate": 0.06})
        self.assertEqual(self.session.rates, Rates(stopped_rate=0.03, moving_rate=0.06))
        self.assertEqual(self.rates_repository.saved, [Rates(stopped_rate=0.03, moving_rate=0.06)])

    def test_put_rates_rejects_non_positive(self):
        response = self.client.put("/api/rates", json={"stopped_rate": 0, "moving_rate": 0.06})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.rates_repository.saved, [])

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
