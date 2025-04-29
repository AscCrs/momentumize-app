from beanie import Document
from pydantic import EmailStr
from datetime import date
from uuid import uuid4, UUID

class UsuarioModel(Document):
    id: UUID = uuid4()
    nombre: str
    correo: EmailStr
    fecha_registro: date

    class Settings:
        name = "usuarios"
