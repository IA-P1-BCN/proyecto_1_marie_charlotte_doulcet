from abc import ABC, abstractmethod


class AccountRepository(ABC):
    """Port: where the account (company + password hash) is stored."""

    @abstractmethod
    def get(self):
        """Return the Account, or None if no password has been set yet."""

    @abstractmethod
    def save(self, account):
        """Store the account, replacing any previous one."""
