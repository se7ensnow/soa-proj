from user_service_app.crud import create_user, get_user_by_username, is_username_taken
from user_service_app.database import get_db
from user_service_app.schemas import UserCreate, UserOut, LoginRequest
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if is_username_taken(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username taken")
    return create_user(db, user_data)

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Login successful", "user_id": user.id}