from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RideRecord:
    """A finished, persisted ride. `id` is assigned by the repository when saved."""

    id: int | None
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    amount: float
