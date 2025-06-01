from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @field_validator('phone_number')
    def validate_phone(cls, phone_number):
        if phone_number is None:
            return phone_number
        if not phone_number.startswith('+') or not phone_number[1:].isdigit() or not (10 <= len(phone_number[1:]) <= 15):
            raise ValueError(f'Invalid phone number: {phone_number}. Phone number should start with + and contain 10-15 digits.')
        return phone_number


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True

class Token(BaseModel):
    access_token: str