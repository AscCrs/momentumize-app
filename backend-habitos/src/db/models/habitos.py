from beanie import Document
from uuid import UUID, uuid4
from datetime import date
from pydantic import Field
from typing import Optional
from enum import Enum


class FrecuenciaEnum(str, Enum):
    diario = "diario"
    semanal = "semanal"
    mensual = "mensual"


class HabitoModel(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    id_usuario: UUID
    id_categoria: Optional[UUID]
    titulo: str
    frecuencia: FrecuenciaEnum
    activo: bool = True
    fecha_creacion: date = Field(default_factory=date.today)

    class Settings:
        name = "habitos"
