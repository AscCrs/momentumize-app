from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# Para creación de una categoría
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# Para actualización de una categoría
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

# Para salida (response) de una categoría
class CategoriaOut(BaseModel):
    id: UUID
    nombre: str
    descripcion: Optional[str] = None
