from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    """The single account of the install. `company` is empty for a password set from the CLI/GUI only."""

    company: str
    password_hash: str

    @property
    def is_registered(self):
        return bool(self.company and self.password_hash)
