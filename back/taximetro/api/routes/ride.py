from fastapi import APIRouter, Depends, HTTPException
from taximetro.api.dependencies import RideServiceDep, require_auth
from taximetro.api.schemas import ActiveRideDTO, ChangeStateRequest, RatesRequest, RideDTO
from taximetro.domain.errors import AlreadyInStateError, NoActiveRideError, RideAlreadyActiveError
from taximetro.domain.rates import Rates

router = APIRouter(prefix="/api/ride", tags=["ride"], dependencies=[Depends(require_auth)])

NO_ACTIVE_RIDE = HTTPException(status_code=404, detail="No active ride")


@router.post("/start", status_code=201)
def start_ride(rides: RideServiceDep, body: RatesRequest | None = None) -> ActiveRideDTO:
    try:
        ride = rides.start_ride(Rates(**body.model_dump()) if body else None)
    except RideAlreadyActiveError:
        raise HTTPException(status_code=409, detail="A ride is already active")
    return ActiveRideDTO.from_ride(ride)


@router.get("")
def get_active_ride(rides: RideServiceDep) -> ActiveRideDTO:
    if not rides.has_active_ride:
        raise NO_ACTIVE_RIDE
    return ActiveRideDTO.from_ride(rides.current_ride)


@router.patch("/state")
def change_state(body: ChangeStateRequest, rides: RideServiceDep) -> ActiveRideDTO:
    try:
        rides.change_state(body.state)
    except NoActiveRideError:
        raise NO_ACTIVE_RIDE
    except AlreadyInStateError:
        raise HTTPException(status_code=409, detail=f"Ride is already {body.state}")
    return ActiveRideDTO.from_ride(rides.current_ride)


@router.post("/end")
def end_ride(rides: RideServiceDep) -> RideDTO:
    try:
        return RideDTO.from_record(rides.end_ride())
    except NoActiveRideError:
        raise NO_ACTIVE_RIDE
