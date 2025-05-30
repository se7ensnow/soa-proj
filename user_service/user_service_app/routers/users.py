from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from user_service_app.crud import update_user
from user_service_app.database import get_db
from user_service_app.models import User
from user_service_app.schemas import UserOut, UserUpdate

router = APIRouter()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user_profile(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user, update_data)