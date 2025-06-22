from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: str
    password: str

class Register(BaseModel):
    nama: str
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: int

class SimpleResponse(BaseModel):
    status: str
    message: str