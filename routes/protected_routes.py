from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from database import sessionlocal
import models

router = APIRouter()

security = HTTPBearer()

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = payload.get("sub")
    session_id = payload.get("session_id")

    db = sessionlocal()

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user.current_session_id != session_id:
        raise HTTPException(
            status_code=401,
            detail="Session expired due to login from another device"
        )

    return user

@router.get("/profile")
def profile(user = Depends(get_current_user)):
    return {
        "name": user.name,
        "email": user.email
    }