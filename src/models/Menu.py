from sqlalchemy import Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from src.enums import StatusMenuEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Pesanan import Pesanan

class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nama: Mapped[str] = mapped_column(String(255), nullable=False)
    harga: Mapped[int] = mapped_column(Integer, nullable=False)
    gambar: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StatusMenuEnum] = mapped_column(SqlEnum(StatusMenuEnum), nullable=False)

    pesanans: Mapped[list['Pesanan']] = relationship('Pesanan', back_populates='menu')