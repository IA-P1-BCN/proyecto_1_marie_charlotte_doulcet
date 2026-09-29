from dataclasses import asdict, dataclass, fields, replace
from taximetro.domain.ride_state import RideState


@dataclass(frozen=True)
class Rates:
    """Price per second for each ride state. Immutable and always valid (positive numbers)."""

    stopped_rate: float
    moving_rate: float

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"Invalid value for {field.name}: must be a positive number")

    def rate_for(self, state):
        return getattr(self, f"{RideState(state).value}_rate")

    def with_rate(self, key, value):
        if key not in {field.name for field in fields(self)}:
            raise ValueError(f"Unknown rate: {key}")
        return replace(self, **{key: value})

    def to_dict(self):
        return asdict(self)
