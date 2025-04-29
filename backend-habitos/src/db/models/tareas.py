from beanie import Document
from uuid import UUID, uuid4
from datetime import date
from pydantic import Field

class TareaModel(Document):
    id: UUID = Field(default_factory=uuid4)
    id_usuario: UUID
    descripcion: str
    fecha_limite: date | None = None
    completada: bool = False
    fecha_creacion: date = Field(default_factory=date.today)

    class Settings:
        name = "tareas"  # nombre de la colección en MongoDB
