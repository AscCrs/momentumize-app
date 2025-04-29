from beanie import Document
from uuid import UUID
from typing import Optional

class CategoriaModel(Document):
    id: UUID
    nombre: str
    descripcion: Optional[str] = None

    class Settings:
        name = "categorias"  # Nombre de la colección en MongoDB
