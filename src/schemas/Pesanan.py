from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from src.enums import StatusPesananEnum
from .Menu import MenuResponse
from .User import UserResponse

class PesananBase(BaseModel):
    user_id: Optional[int]
    menu_id: Optional[int]
    status: StatusPesananEnum

class PesananCreate(BaseModel):
    user_id: Optional[int]
    menu_ids: Optional[List[int]]
    status: StatusPesananEnum

class PesananUpdate(BaseModel):
    user_id: Optional[int]
    menu_id: Optional[int]
    status: StatusPesananEnum

class PesananResponse(PesananBase):
    id: str
    created_at: datetime
    menu: Optional[MenuResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class UserPesanan(BaseModel):
    id: str
    created_at: datetime
    status: StatusPesananEnum
    menu: Optional[MenuResponse] = None