from abc import ABC, abstractmethod


class RideRepository(ABC):
    """Port: how finished rides are stored. The domain depends on this, never on SQLite."""

    @abstractmethod
    def save(self, ride):
        """Persist a finished Ride and return its RideRecord (with the generated id)."""

    @abstractmethod
    def find_by_id(self, ride_id):
        """Return the RideRecord, or None if unknown."""

    @abstractmethod
    def find_by_date(self, day):
        """Return the RideRecords that started on `day` (a datetime.date)."""
