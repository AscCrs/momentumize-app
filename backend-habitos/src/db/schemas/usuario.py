from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr

class UsuarioOut(BaseModel):
    id: str
    nombre: str
    correo: EmailStr
    fecha_registro: date

class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    correo: Optional[EmailStr]
