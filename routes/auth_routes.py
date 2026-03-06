from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from core.security import verify_password
from auth import create_access_token
import models, schemas

from core.security import hash_password
from database import sessionlocal 
router = APIRouter()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    db_user.current_session_id = session_id
    db.commit()

    token = create_access_token({
        "sub": str(db_user.id),
        "session_id": session_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }