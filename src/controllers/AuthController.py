from sqlalchemy.orm import Session
from src.models import User
from src.schemas import Login, Register
from src.enums import RoleEnum
import secrets

class AuthController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def userLogin(self, request: Login):
        user = self.db.query(User).filter(
            (User.email == request.email) & (User.role != RoleEnum.ADMIN)
        ).first()

        if not user or user.password != request.password:
            return None
        token = secrets.token_hex(16)
        user.token = token
        self.db.commit()

        return {
            'token': token,
            'user_id': user.id
        }
    
    def adminLogin(self, request: Login):
        user = self.db.query(User).filter(
            (User.email == request.email) & (User.role == RoleEnum.ADMIN)
        ).first()

        if not user or user.password != request.password:
            return None
        token = secrets.token_hex(16)
        user.token = token
        self.db.commit()

        return {
            'token': token,
            'user_id': user.id
        }
    
    def register(self, request: Register):
        new_user = User(
            nama=request.nama,
            email=request.email,
            password=request.password,
            role=RoleEnum.USER
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def logout(self, user_id: str):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None
        
        user.token = ''
        self.db.commit()

        return {
            'status': 'success',
            'message': 'logout berhasil'
        }