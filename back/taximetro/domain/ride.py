import time

class Ride:
    def __init__(self, rates, started_at=None):
        self.rates = rates
        self.started_at = started_at if started_at is not None else time.time()
        self.state = "stopped"
        self.segment_start = self.started_at
        self.accumulated = 0.0
        self.ended_at = None

    def _calculate_segment(self, duration_seconds):
        rate = self.rates[f"{self.state}_rate"]
        return duration_seconds * rate

    def get_total(self, now=None):
          now = now if now is not None else time.time()
          current_segment_duration = now - self.segment_start
          current_segment_amount = self._calculate_segment(current_segment_duration)
          return self.accumulated + current_segment_amount

    def toggle_state(self, new_state, now=None):
          if new_state == self.state:
              return         
          now = now if now is not None else time.time()
          segment_duration = now - self.segment_start
          self.accumulated += self._calculate_segment(segment_duration)
          self.state = new_state
          self.segment_start = now 

    def end(self, now=None):
        now = now if now is not None else time.time()
        segment_duration  = now - self.segment_start
        self.accumulated += self._calculate_segment(segment_duration)
        self.ended_at = now 

        return self.accumulated

    def format_total(self):
        return f"{self.accumulated:.2f}"

    def get_duration_seconds(self):
        if self.ended_at is None:
            return 0
        return round(self.ended_at - self.started_at)
            
