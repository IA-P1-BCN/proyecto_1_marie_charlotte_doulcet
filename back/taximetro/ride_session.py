from taximetro.domain.ride import Ride
from taximetro.infrastructure.rates_config import save_rates


class NoActiveRideError(Exception):
    pass

class RideAlreadyActiveError(Exception):
    pass

class AlreadyInStateError(Exception):
    def __init__(self, state):
        self.state = state
        super().__init__(f"Already in state: {state}")

class RideSession:
    def __init__(self, rates, storage):
        self.rates = rates
        self.storage = storage
        self.current_ride = None

    @property
    def has_active_ride(self):
        return self.current_ride is not None

    def start_ride(self):
        if self.has_active_ride:
            raise RideAlreadyActiveError()
        self.current_ride = Ride(self.rates)
        return self.current_ride

    def change_state(self, new_state):
        if not self.has_active_ride:
            raise NoActiveRideError()
        if self.current_ride.state == new_state:
            raise AlreadyInStateError(new_state)
        self.current_ride.toggle_state(new_state)

    def end_ride(self):
        if not self.has_active_ride:
            raise NoActiveRideError()
        ride = self.current_ride
        ride.end()
        self.storage.save_ride(ride)
        self.current_ride = None
        return ride

    def change_rate(self, rate_key, new_value):
        updated_rates = {**self.rates, rate_key: new_value}
        save_rates(updated_rates)
        self.rates = updated_rates

    def get_today_history(self):
        return self.storage.load_today()