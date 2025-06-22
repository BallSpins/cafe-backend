import os
import time
import shutil
import ulid
from fastapi import UploadFile, File, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')

def get_db():
    from src.database import Sessionlocal
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def generate_ulid() -> str:
    return str(ulid.new())

async def save_image(nama: str, path: str, image: UploadFile = File(...)):
    if image.filename:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        file_extension = os.path.splitext(image.filename)[1]
        filename = f"{nama.replace(' ', '_')}_{int(time.time())}{file_extension}"
        
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, filename)

        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f'/{path}/{filename}'

        return image_url
    else:
        return None
    
async def is_admin(admin_token: str = Header(None)):
    if admin_token == ADMIN_TOKEN:
        return True
    raise HTTPException(status_code=403, detail='Akses ditolak')

def get_current_user(user_token: str = Header(None), db: Session = Depends(get_db)):
    from src.models import User
    
    if not user_token:
        raise HTTPException(status_code=401, detail='Token tidak ditemukan')
    
    user = db.query(User).filter(User.token == user_token).first()
    if not user:
        raise HTTPException(status_code=401, detail='Token tidak valid')
    
    print(user.__dict__)

    return user