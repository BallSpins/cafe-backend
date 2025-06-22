from sqlalchemy import Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from src.enums import RoleEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Pesanan import Pesanan

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nama: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=True)

    pesanans: Mapped[list['Pesanan']] = relationship('Pesanan', back_populates='user')