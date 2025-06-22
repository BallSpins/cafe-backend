from typing import Optional, List
from pydantic import BaseModel, EmailStr
from src.enums import RoleEnum

class UserBase(BaseModel):
    nama: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nama: Optional[str]
    email: Optional[EmailStr]
    role: Optional[RoleEnum]

class UserUpdatePassword(BaseModel):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserPesananResponse(UserResponse):
    pesanans: List['UserPesanan']

from .Pesanan import UserPesanan