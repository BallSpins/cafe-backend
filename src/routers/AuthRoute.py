from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import Login, Register, AuthResponse, SimpleResponse, UserResponse
from src.controllers import AuthController
from src.database import Sessionlocal

router = APIRouter(prefix='/auth', tags=['auth'])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(db)

@router.post('/register', response_model=UserResponse)
def register(request: Register, controller: AuthController = Depends(get_auth_controller)):
    try:
        response = controller.register(request)
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/admin/login', response_model=AuthResponse)
def admin_login(request: Login, controller: AuthController = Depends(get_auth_controller)):
    try:
        response = controller.adminLogin(request)
        if response is None:
            raise HTTPException(status_code=404, detail='User tidak ditemukan')
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/user/login', response_model=AuthResponse)
def user_login(request: Login, controller: AuthController = Depends(get_auth_controller)):
    try:
        response = controller.userLogin(request)
        if response is None:
            raise HTTPException(status_code=404, detail='User tidak ditemukan')
        return response
    except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/logout/{user_id}', response_model=SimpleResponse)
def logout(user_id: str, controller: AuthController = Depends(get_auth_controller)):
    try:
        response = controller.logout(user_id)
        if response is None:
            raise HTTPException(status_code=404, detail='User tidak ditemukan')
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))