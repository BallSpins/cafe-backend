from sqlalchemy.orm import Session, joinedload
from src.models import User, Pesanan
from src.schemas import UserCreate, UserUpdate, UserUpdatePassword

class UserController:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_all(self):
        return self.db.query(User).all()
    
    def get_by_id(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_id_with_pesanan(self, user_id: str):
        return self.db.query(User).options(
            joinedload(User.pesanans).joinedload(Pesanan.menu)
        ).filter(User.id == user_id).first()
    
    def create(self, request: UserCreate):
        new_user = User(
            nama=request.nama,
            email=request.email,
            password=request.password,
            role=request.role
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update(self, user_id: str, request: UserUpdate):
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user
    
    def reset_password(self, user_id: str, request: UserUpdatePassword):
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        user.password = request.password

        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str):
        user = self.get_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user