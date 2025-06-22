from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import PesananCreate, PesananResponse, PesananUpdate
from src.controllers import PesananController
from src.database import Sessionlocal
from src.utils import is_admin

router = APIRouter(prefix='/pesanan', tags=['pesanan'])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_pesanan_controller(db: Session = Depends(get_db)) -> PesananController:
    return PesananController(db)

@router.get('/', response_model=list[PesananResponse], dependencies=[Depends(is_admin)])
def list_pesanan(controller: PesananController = Depends(get_pesanan_controller)):
    try:
        return controller.get_all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{pesanan_id}', response_model=PesananResponse, dependencies=[Depends(is_admin)])
def get_pesanan(pesanan_id: str, controller: PesananController = Depends(get_pesanan_controller)):
    try:
        pesanan = controller.get_by_id(pesanan_id)
        if not pesanan:
            raise HTTPException(status_code=404, detail='Pesanan not found')
        return pesanan
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/', response_model=list[PesananResponse])
def create_pesanan(request: PesananCreate, controller: PesananController = Depends(get_pesanan_controller)):
    try:
        return controller.create(request)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{pesanan_id}', response_model=PesananResponse, dependencies=[Depends(is_admin)])
def update_pesanan(pesanan_id: str, request: PesananUpdate, controller: PesananController = Depends(get_pesanan_controller)):
    try:
        pesanan = controller.update(pesanan_id, request)
        if not pesanan:
            raise HTTPException(status_code=404, detail='Pesanan not found')
        return pesanan
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{pesanan_id}', response_model=PesananResponse, dependencies=[Depends(is_admin)])
def delete_pesanan(pesanan_id: str, controller: PesananController = Depends(get_pesanan_controller)):
    try:
        pesanan = controller.delete(pesanan_id)
        if not pesanan:
            raise HTTPException(status_code=404, detail='Pesanan not found')
        return pesanan
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
