from datetime import datetime, date as date_cls
from pathlib import Path
from typing import Literal
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from taximetro.infrastructure.rates_config import load_rates
from taximetro.infrastructure.storage.db_storage import DbStorage
from taximetro.ride_session import RideSession, NoActiveRideError, RideAlreadyActiveError, AlreadyInStateError

app = FastAPI(title="Taximetro API")

_session = None

def get_session():
    global _session
    if _session is None:
        _session = RideSession(load_rates(), DbStorage())
    return _session

class ChangeStateRequest(BaseModel):
    state: Literal["stopped", "moving"]

class RatesRequest(BaseModel):
    stopped_rate: float = Field(gt=0)
    moving_rate: float = Field(gt=0)

def _active_ride_dto(ride):
    return {
        "state": ride.state,
        "started_at": datetime.fromtimestamp(ride.started_at).isoformat(),
        "amount_so_far": round(ride.get_total(), 2),
        "elapsed_seconds": round(time.time() - ride.started_at),
        "current_rate": ride.rates[f"{ride.state}_rate"],
    }

def _row_to_ride_dto(row):
    return {
        "id": row["id"],
        "started_at": row["started_at"],
        "ended_at": row["ended_at"],
        "duration_seconds": row["duration_seconds"],
        "amount": row["amount"],
    }

@app.post("/api/ride/start", status_code=201)
def start_ride(body: RatesRequest | None = None, session: RideSession = Depends(get_session)):
    try:
        ride = session.start_ride(body.model_dump() if body else None)
    except RideAlreadyActiveError:
        raise HTTPException(status_code=409, detail="A ride is already active")
    return _active_ride_dto(ride)

@app.get("/api/ride")
def get_active_ride(session: RideSession = Depends(get_session)):
    if not session.has_active_ride:
        raise HTTPException(status_code=404, detail="No active ride")
    return _active_ride_dto(session.current_ride)

@app.patch("/api/ride/state")
def change_state(body: ChangeStateRequest, session: RideSession = Depends(get_session)):
    try:
        session.change_state(body.state)
    except NoActiveRideError:
        raise HTTPException(status_code=404, detail="No active ride")
    except AlreadyInStateError:
        raise HTTPException(status_code=409, detail=f"Ride is already {body.state}")
    return _active_ride_dto(session.current_ride)

@app.post("/api/ride/end")
def end_ride(session: RideSession = Depends(get_session)):
    try:
        session.end_ride()
    except NoActiveRideError:
        raise HTTPException(status_code=404, detail="No active ride")
    row = session.storage.load_by_id(session.storage.last_inserted_id)
    return _row_to_ride_dto(row)

@app.get("/api/rides")
def list_rides(date: str = None, session: RideSession = Depends(get_session)):
    target_date = date or date_cls.today().isoformat()
    rows = session.storage.load_by_date(target_date)
    return [_row_to_ride_dto(row) for row in rows]

@app.get("/api/rides/{ride_id}")
def get_ride(ride_id: int, session: RideSession = Depends(get_session)):
    row = session.storage.load_by_id(ride_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return _row_to_ride_dto(row)

@app.get("/api/rates")
def get_rates(session: RideSession = Depends(get_session)):
    return session.rates

@app.put("/api/rates")
def update_rates(body: RatesRequest, session: RideSession = Depends(get_session)):
    # Applies to the next ride: the running one keeps the rates it started with.
    for key, value in body.model_dump().items():
        session.change_rate(key, value)
    return session.rates

# Prod only: serve the React build. Mounted last so it never shadows /api routes.
# Skipped if front/dist doesn't exist, so `uvicorn --reload` still works during frontend dev.
_dist_dir = Path(__file__).resolve().parent.parent.parent / "front" / "dist"
if _dist_dir.is_dir():
    app.mount("/", StaticFiles(directory=_dist_dir, html=True), name="web-panel")
