import time
from taximetro.domain.ride_state import RideState


class Ride:
    """A ride in progress: accumulates the price segment by segment, per state."""

    def __init__(self, rates, started_at=None):
        self.rates = rates
        self.started_at = started_at if started_at is not None else time.time()
        self.state = RideState.STOPPED
        self.segment_start = self.started_at
        self.accumulated = 0.0
        self.ended_at = None

    def _close_segment(self, now):
        self.accumulated += (now - self.segment_start) * self.rates.rate_for(self.state)
        self.segment_start = now

    def get_total(self, now=None):
        now = now if now is not None else time.time()
        return self.accumulated + (now - self.segment_start) * self.rates.rate_for(self.state)

    def toggle_state(self, new_state, now=None):
        new_state = RideState(new_state)
        if new_state is self.state:
            return
        self._close_segment(now if now is not None else time.time())
        self.state = new_state

    def end(self, now=None):
        now = now if now is not None else time.time()
        self._close_segment(now)
        self.ended_at = now
        return self.accumulated

    def get_duration_seconds(self):
        if self.ended_at is None:
            return 0
        return round(self.ended_at - self.started_at)
