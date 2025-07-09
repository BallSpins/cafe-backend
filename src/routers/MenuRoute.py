from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import MenuCreate, MenuResponse, MenuUpdate
from src.controllers import MenuController
from src.database import Sessionlocal
from src.enums import StatusMenuEnum
from src.utils import save_image, is_admin
from typing import Optional

router = APIRouter(prefix='/menu', tags=['menu'])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_menu_controller(db: Session = Depends(get_db)) -> MenuController:
    return MenuController(db)

@router.get('/', response_model=list[MenuResponse])
def list_menu(controller: MenuController = Depends(get_menu_controller)):
    try:
        return controller.get_all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/{menu_id}', response_model=MenuResponse)
def get_menu(menu_id: str, controller: MenuController = Depends(get_menu_controller)):
    try:
        menu = controller.get_by_id(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        return menu
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/', response_model=MenuResponse, dependencies=[Depends(is_admin)])
async def create_menu(
    nama: str = Form(...),
    harga: int = Form(...),
    status: StatusMenuEnum = Form(...),
    image: UploadFile = File(...),
    controller: MenuController = Depends(get_menu_controller)
    ):
    try:
        image_info = await save_image(nama, 'media/menu', image)
        if image_info:
            request = MenuCreate(
                nama=nama,
                harga=harga,
                status=status
                )
            
            return controller.create(request, image_info)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put('/{menu_id}', response_model=MenuResponse, dependencies=[Depends(is_admin)])
async def update_menu(
    menu_id: str, 
    nama: Optional[str] = Form(None),
    harga: Optional[int] = Form(None),
    status: Optional[StatusMenuEnum] = Form(None),
    image: Optional[UploadFile] = File(None), 
    controller: MenuController = Depends(get_menu_controller)
    ):
    try:
        update_data = {}
        if nama is not None:
            update_data['nama'] = nama
        if harga is not None:
            update_data['harga'] = harga
        if status is not None:
            update_data['status'] = status

        if image and nama:
            image_info = await save_image(nama, 'media/menu', image)
            if image_info:
                update_data['gambar'] = image_info

        req = MenuUpdate(**update_data)
        updated_menu = controller.update(menu_id, req)
        return updated_menu
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete('/{menu_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin)])
def delete_menu(menu_id: str, controller: MenuController = Depends(get_menu_controller)):
    try:
        menu = controller.delete(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        return
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))