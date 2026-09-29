from datetime import date as date_cls
from fastapi import APIRouter, Depends, HTTPException
from taximetro.api.dependencies import RideServiceDep, require_auth
from taximetro.api.schemas import RideDTO

router = APIRouter(prefix="/api/rides", tags=["history"], dependencies=[Depends(require_auth)])


@router.get("")
def list_rides(rides: RideServiceDep, date: date_cls | None = None) -> list[RideDTO]:
    return [RideDTO.from_record(record) for record in rides.get_history(date or date_cls.today())]


@router.get("/{ride_id}")
def get_ride(ride_id: int, rides: RideServiceDep) -> RideDTO:
    record = rides.get_ride(ride_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return RideDTO.from_record(record)
