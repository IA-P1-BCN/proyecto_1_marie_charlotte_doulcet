from datetime import date as date_cls, datetime
from pathlib import Path
from typing import Literal
import time
import secrets
from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from taximetro.infrastructure.auth import hash_password, check_password, is_registered, save_account, load_password_hash, check_company
from taximetro.infrastructure.rates_config import load_rates
from taximetro.domain.errors import AlreadyInStateError, NoActiveRideError, RideAlreadyActiveError
from taximetro.domain.rates import Rates
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository
from taximetro.ride_session import RideSession

app = FastAPI(title="Taximetro API")

AUTH_PATH = "auth.ini"
_tokens = set()  # ponytail: in-memory session tokens, lost on restart; persist/expire if that matters
_session = None

def require_auth(authorization: str = Header(default="")):
    if authorization.removeprefix("Bearer ") not in _tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

protected = APIRouter(dependencies=[Depends(require_auth)])

def get_session():
    global _session
    if _session is None:
        _session = RideSession(load_rates(), SqliteRideRepository())
    return _session

class ChangeStateRequest(BaseModel):
    state: Literal["stopped", "moving"]

class CredentialsRequest(BaseModel):
    company: str
    password: str

def _new_token():
    token = secrets.token_urlsafe(32)
    _tokens.add(token)
    return {"token": token}

class RatesRequest(BaseModel):
    stopped_rate: float = Field(gt=0)
    moving_rate: float = Field(gt=0)

def _active_ride_dto(ride):
    return {
        "state": ride.state,
        "started_at": datetime.fromtimestamp(ride.started_at).isoformat(),
        "amount_so_far": round(ride.get_total(), 2),
        "elapsed_seconds": round(time.time() - ride.started_at),
        "current_rate": ride.rates.rate_for(ride.state),
    }

def _record_dto(record):
    return {
        "id": record.id,
        "started_at": record.started_at.isoformat(),
        "ended_at": record.ended_at.isoformat(),
        "duration_seconds": record.duration_seconds,
        "amount": record.amount,
    }

@protected.post("/api/ride/start", status_code=201)
def start_ride(body: RatesRequest | None = None, session: RideSession = Depends(get_session)):
    try:
        ride = session.start_ride(Rates(**body.model_dump()) if body else None)
    except RideAlreadyActiveError:
        raise HTTPException(status_code=409, detail="A ride is already active")
    return _active_ride_dto(ride)

@protected.get("/api/ride")
def get_active_ride(session: RideSession = Depends(get_session)):
    if not session.has_active_ride:
        raise HTTPException(status_code=404, detail="No active ride")
    return _active_ride_dto(session.current_ride)

@protected.patch("/api/ride/state")
def change_state(body: ChangeStateRequest, session: RideSession = Depends(get_session)):
    try:
        session.change_state(body.state)
    except NoActiveRideError:
        raise HTTPException(status_code=404, detail="No active ride")
    except AlreadyInStateError:
        raise HTTPException(status_code=409, detail=f"Ride is already {body.state}")
    return _active_ride_dto(session.current_ride)

@protected.post("/api/ride/end")
def end_ride(session: RideSession = Depends(get_session)):
    try:
        record = session.end_ride()
    except NoActiveRideError:
        raise HTTPException(status_code=404, detail="No active ride")
    return _record_dto(record)

@protected.get("/api/rides")
def list_rides(date: date_cls | None = None, session: RideSession = Depends(get_session)):
    records = session.get_history(date or date_cls.today())
    return [_record_dto(record) for record in records]

@protected.get("/api/rides/{ride_id}")
def get_ride(ride_id: int, session: RideSession = Depends(get_session)):
    record = session.get_ride(ride_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return _record_dto(record)

@protected.get("/api/rates")
def get_rates(session: RideSession = Depends(get_session)):
    return session.rates.to_dict()

@protected.put("/api/rates")
def update_rates(body: RatesRequest, session: RideSession = Depends(get_session)):
    # Applies to the next ride: the running one keeps the rates it started with.
    session.set_rates(Rates(**body.model_dump()))
    return session.rates.to_dict()

@app.get("/api/auth/status")
def auth_status():
    return {"registered": is_registered(AUTH_PATH)}

@app.post("/api/auth/setup", status_code=201)
def auth_setup(body: CredentialsRequest):
    if is_registered(AUTH_PATH):
        raise HTTPException(status_code=409, detail="Account already registered")
    company, password = body.company.strip(), body.password.strip()
    if not company or not password:
        raise HTTPException(status_code=422, detail="Company and password must not be blank")
    # Also replaces a password created earlier from the CLI/GUI (same auth.ini).
    save_account(company, hash_password(password), AUTH_PATH)
    return _new_token()

@app.post("/api/auth/login")
def auth_login(body: CredentialsRequest):
    if not is_registered(AUTH_PATH):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    password_ok = check_password(body.password.strip(), load_password_hash(AUTH_PATH))
    if not (check_company(body.company, AUTH_PATH) and password_ok):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    return _new_token()

app.include_router(protected)

# Prod only: serve the React build. Mounted last so it never shadows /api routes.
# Skipped if front/dist doesn't exist, so `uvicorn --reload` still works during frontend dev.
_dist_dir = Path(__file__).resolve().parent.parent.parent / "front" / "dist"
if _dist_dir.is_dir():
    app.mount("/", StaticFiles(directory=_dist_dir, html=True), name="web-panel")
