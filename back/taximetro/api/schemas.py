import time
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from taximetro.domain.ride_state import RideState


class ChangeStateRequest(BaseModel):
    state: Literal["stopped", "moving"]


class CredentialsRequest(BaseModel):
    company: str
    password: str


class RatesRequest(BaseModel):
    stopped_rate: float = Field(gt=0, allow_inf_nan=False)
    moving_rate: float = Field(gt=0, allow_inf_nan=False)


class RatesDTO(BaseModel):
    stopped_rate: float
    moving_rate: float


class TokenDTO(BaseModel):
    token: str


class AuthStatusDTO(BaseModel):
    registered: bool


class ActiveRideDTO(BaseModel):
    state: RideState
    started_at: str
    amount_so_far: float
    elapsed_seconds: int
    current_rate: float

    @classmethod
    def from_ride(cls, ride):
        return cls(
            state=ride.state,
            started_at=datetime.fromtimestamp(ride.started_at).isoformat(),
            amount_so_far=round(ride.get_total(), 2),
            elapsed_seconds=round(time.time() - ride.started_at),
            current_rate=ride.rates.rate_for(ride.state),
        )


class RideDTO(BaseModel):
    id: int
    started_at: str
    ended_at: str
    duration_seconds: float
    amount: float

    @classmethod
    def from_record(cls, record):
        return cls(
            id=record.id,
            started_at=record.started_at.isoformat(),
            ended_at=record.ended_at.isoformat(),
            duration_seconds=record.duration_seconds,
            amount=record.amount,
        )
