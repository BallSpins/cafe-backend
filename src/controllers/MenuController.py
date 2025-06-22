from sqlalchemy.orm import Session
from src.models import Menu
from src.schemas import MenuCreate, MenuUpdate

class MenuController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self):
        return self.db.query(Menu).all()
    
    def get_by_id(self, menu_id: str):
        return self.db.query(Menu).filter(Menu.id == menu_id).first()
    
    def create(self, request: MenuCreate, image_url: str):
        new_menu = Menu(
            nama=request.nama,
            harga=request.harga,
            gambar=image_url,
            status=request.status
        )

        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu
    
    def update(self, menu_id: str, request: MenuUpdate):
        menu = self.get_by_id(menu_id)
        if not menu:
            return None
        
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(menu, key):
                setattr(menu, key, value)

        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def delete(self, menu_id: str):
        menu = self.get_by_id(menu_id)
        if not menu:
            return None
        self.db.delete(menu)
        self.db.commit()
        return menu
