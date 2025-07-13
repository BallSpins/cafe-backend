from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import UserCreate, UserResponse, UserUpdate, UserUpdatePassword, UserPesananResponse
from src.controllers import UserController
from src.database import Sessionlocal
from src.utils import is_admin, get_current_user
from src.models import User

router = APIRouter(prefix='/user', tags=['user'])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

@router.get('/', response_model=list[UserResponse], dependencies=[Depends(is_admin)])
def list_user(controller: UserController = Depends(get_user_controller)):
    try:
        return controller.get_all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/{user_id}', response_model=UserResponse, dependencies=[Depends(is_admin)])
def get_user(user_id: str, controller: UserController = Depends(get_user_controller)):
    try:
        user = controller.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{user_id}/pesanan', response_model=UserPesananResponse)
def get_user_with_order(
    user_id: str, 
    controller: UserController = Depends(get_user_controller),
    current_user: User = Depends(get_current_user)
):
    print('ini di rute, curr id:', current_user.id)
    print('ini di rute, id:', user_id)

    if str(current_user.id) != user_id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Akses ditolak')
    
    try:
        user = controller.get_by_id_with_pesanan(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/', response_model=UserResponse, dependencies=[Depends(is_admin)])
def create_user(request: UserCreate, controller: UserController = Depends(get_user_controller)):
    try:
        return controller.create(request)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{user_id}', response_model=UserResponse, dependencies=[Depends(is_admin)])
def update_user(user_id: str, request: UserUpdate, controller: UserController = Depends(get_user_controller)):
    try:
        user = controller.update(user_id, request)
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put('/{user_id}/reset', response_model=UserResponse)
def reset_password(
    user_id: str,
    request: UserUpdatePassword, 
    controller: UserController = Depends(get_user_controller),
    current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Akses ditolak')
    
    try:
        
        user = controller.reset_password(user_id, request)
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin)])
def delete_user(
    user_id: str, 
    controller: UserController = Depends(get_user_controller),
):  
    try:
        user = controller.delete(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))