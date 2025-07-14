import ulid
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.enums import StatusPesananEnum

def generate_ulid():
    return str(ulid.new())

class Pesanan(Base):
    __tablename__ = 'pesanan'

    id: Mapped[str] = mapped_column(String(26), primary_key=True, index=True, default=generate_ulid)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    menu_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('menu.id', ondelete='SET NULL'), nullable=True)
    status: Mapped[StatusPesananEnum] = mapped_column(SqlEnum(StatusPesananEnum), nullable=False)
    harga: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship('User', back_populates='pesanans')
    menu = relationship('Menu', back_populates='pesanans')