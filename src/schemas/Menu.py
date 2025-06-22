from typing import Optional
from pydantic import BaseModel
from src.enums import StatusMenuEnum

class MenuBase(BaseModel):
    nama: str
    harga: int
    status: StatusMenuEnum

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    nama: Optional[str]
    harga: Optional[int]
    status: Optional[StatusMenuEnum]

class MenuResponse(MenuBase):
    id: int
    gambar: str

    class Config:
        from_attributes = True