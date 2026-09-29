from datetime import date
from taximetro.domain.errors import AlreadyInStateError, NoActiveRideError, RideAlreadyActiveError
from taximetro.domain.ride import Ride


class RideService:
    """Use cases around the single ride in progress, the default rates and the ride history."""

    def __init__(self, rates_repository, ride_repository):
        self._rates_repository = rates_repository
        self._ride_repository = ride_repository
        self.rates = rates_repository.load()
        self.current_ride = None

    @property
    def has_active_ride(self):
        return self.current_ride is not None

    def start_ride(self, rates=None):
        if self.has_active_ride:
            raise RideAlreadyActiveError()
        self.current_ride = Ride(rates or self.rates)
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
        record = self._ride_repository.save(ride)
        self.current_ride = None
        return record

    def change_rate(self, rate_key, new_value):
        self.set_rates(self.rates.with_rate(rate_key, new_value))

    def set_rates(self, rates):
        self._rates_repository.save(rates)
        self.rates = rates

    def get_today_history(self):
        return self.get_history(date.today())

    def get_history(self, day):
        return self._ride_repository.find_by_date(day)

    def get_ride(self, ride_id):
        return self._ride_repository.find_by_id(ride_id)
