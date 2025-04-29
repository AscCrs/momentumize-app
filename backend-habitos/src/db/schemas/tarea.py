from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

# Crear tarea
class TareaCreate(BaseModel):
    id_usuario: UUID
    descripcion: str
    fecha_limite: date | None = None

# Actualizar tarea
class TareaUpdate(BaseModel):
    descripcion: str | None = None
    fecha_limite: date | None = None
    completada: bool | None = None

# Salida (respuesta)
class TareaOut(BaseModel):
    id: UUID
    id_usuario: UUID
    descripcion: str
    fecha_limite: date | None
    completada: bool
    fecha_creacion: date
