from fastapi import APIRouter, HTTPException
from taximetro.api.dependencies import AuthServiceDep
from taximetro.api.schemas import AuthStatusDTO, CredentialsRequest, TokenDTO
from taximetro.domain.errors import AlreadyRegisteredError, BlankCredentialsError, InvalidCredentialsError

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/status")
def auth_status(auth: AuthServiceDep) -> AuthStatusDTO:
    return AuthStatusDTO(registered=auth.is_registered())


@router.post("/setup", status_code=201)
def auth_setup(body: CredentialsRequest, auth: AuthServiceDep) -> TokenDTO:
    try:
        return TokenDTO(token=auth.register(body.company, body.password))
    except AlreadyRegisteredError:
        raise HTTPException(status_code=409, detail="Account already registered")
    except BlankCredentialsError:
        raise HTTPException(status_code=422, detail="Company and password must not be blank")


@router.post("/login")
def auth_login(body: CredentialsRequest, auth: AuthServiceDep) -> TokenDTO:
    try:
        return TokenDTO(token=auth.login(body.company, body.password))
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Wrong credentials")
