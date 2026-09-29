from fastapi import APIRouter, Depends
from taximetro.api.dependencies import RideServiceDep, require_auth
from taximetro.api.schemas import RatesDTO, RatesRequest
from taximetro.domain.rates import Rates

router = APIRouter(prefix="/api/rates", tags=["rates"], dependencies=[Depends(require_auth)])


@router.get("")
def get_rates(rides: RideServiceDep) -> RatesDTO:
    return RatesDTO(**rides.rates.to_dict())


@router.put("")
def update_rates(body: RatesRequest, rides: RideServiceDep) -> RatesDTO:
    # Applies to the next ride: the running one keeps the rates it started with.
    rides.set_rates(Rates(**body.model_dump()))
    return RatesDTO(**rides.rates.to_dict())
