from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime

from user_service_app.auth_utils.jwt import verify_jwt_token, create_access_token
from user_service_app.crud import create_user, get_user_by_username, is_username_taken
from user_service_app.database import get_db
from user_service_app.schemas import UserCreate, UserOut, Token
from user_service_app.user_kafka.user_producer import send_event

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if is_username_taken(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username taken")
    new_user = create_user(db, user_data)
    send_event(
        topic="register",
        event_data={
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "timestamp": datetime.now().isoformat(),
        }
    )
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify")
def verify_token(token: Token):
    payload = verify_jwt_token(token.access_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {"user_id": payload.get("sub")}