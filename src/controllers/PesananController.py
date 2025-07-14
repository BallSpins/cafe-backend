from sqlalchemy.orm import Session, joinedload
from src.models import Pesanan
from src.schemas import PesananCreate, PesananUpdate
from src.utils import generate_ulid

class PesananController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self):
        return self.db.query(Pesanan).options(
            joinedload(Pesanan.user),
            joinedload(Pesanan.menu)
        ).all()
    
    def get_by_id(self, pesanan_id: str):
        return self.db.query(Pesanan).options(
            joinedload(Pesanan.user),
            joinedload(Pesanan.menu)
        ).filter(Pesanan.id == pesanan_id).first()
    
    def create(self, request: PesananCreate):
        new_pesanans = []
        if request.menu_ids:
            for menu_id in request.menu_ids:
                menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
                if not menu:
                    continue
                new_pesanan = Pesanan(
                    id=generate_ulid(),
                    user_id=request.user_id,
                    menu_id=menu_id,
                    status=request.status,
                    harga=menu.harga
                )

                self.db.add(new_pesanan)
                new_pesanans.append(new_pesanan)
            self.db.commit()

            for np in new_pesanans:
                self.db.refresh(new_pesanan)
            return new_pesanans
        else:
            return None
    
    def update(self, pesanan_id: str, request: PesananUpdate):
        pesanan = self.get_by_id(pesanan_id)
        if not pesanan:
            return None
        
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(pesanan, key):
                setattr(pesanan, key, value)

        self.db.commit()
        self.db.refresh(pesanan)
        return pesanan
    
    def delete(self, pesanan_id: str):
        pesanan = self.get_by_id(pesanan_id)
        if not pesanan:
            return None
        self.db.delete(pesanan)
        self.db.commit()
        return pesanan
