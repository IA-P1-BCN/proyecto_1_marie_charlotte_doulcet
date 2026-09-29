from abc import ABC, abstractmethod


class RatesRepository(ABC):
    """Port: where the default rates are stored."""

    @abstractmethod
    def load(self):
        """Return the default Rates. Raises ValueError if missing or invalid."""

    @abstractmethod
    def save(self, rates):
        """Store the given Rates as the new defaults."""
