"""In-memory implementations of the ports, so services and adapters can be tested without files."""
from datetime import datetime
from taximetro.domain.account_repository import AccountRepository
from taximetro.domain.rates_repository import RatesRepository
from taximetro.domain.ride_record import RideRecord
from taximetro.domain.ride_repository import RideRepository


class InMemoryRideRepository(RideRepository):
    def __init__(self):
        self.records = []

    def save(self, ride):
        record = RideRecord(
            id=len(self.records) + 1,
            started_at=datetime.fromtimestamp(ride.started_at),
            ended_at=datetime.fromtimestamp(ride.ended_at),
            duration_seconds=ride.get_duration_seconds(),
            amount=round(ride.accumulated, 2),
        )
        self.records.append(record)
        return record

    def find_by_id(self, ride_id):
        return next((r for r in self.records if r.id == ride_id), None)

    def find_by_date(self, day):
        return [r for r in self.records if r.started_at.date() == day]


class InMemoryRatesRepository(RatesRepository):
    def __init__(self, rates):
        self.rates = rates
        self.saved = []

    def load(self):
        return self.rates

    def save(self, rates):
        self.rates = rates
        self.saved.append(rates)


class InMemoryAccountRepository(AccountRepository):
    def __init__(self, account=None):
        self.account = account

    def get(self):
        return self.account

    def save(self, account):
        self.account = account


class FakePasswordHasher:
    """Instant stand-in for PBKDF2 (600k iterations makes real hashing slow in tests)."""

    def hash(self, password):
        return f"fake${password}"

    def verify(self, password, stored_hash):
        return stored_hash == f"fake${password}"

    def is_valid_hash(self, stored_hash):
        return "$" in stored_hash
