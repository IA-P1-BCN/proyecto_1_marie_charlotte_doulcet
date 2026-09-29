from enum import Enum


class RideState(str, Enum):
    """State of a running ride. `str` mixin: equals its JSON value ("stopped"/"moving")."""

    STOPPED = "stopped"
    MOVING = "moving"
