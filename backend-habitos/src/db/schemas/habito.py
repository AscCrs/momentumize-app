from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum

class FrecuenciaEnum(str, Enum):
    diario = "diario"
    semanal = "semanal"
    mensual = "mensual"


class HabitoBase(BaseModel):
    titulo: str
    frecuencia: FrecuenciaEnum
    activo: bool = True
    id_categoria: Optional[UUID]


class HabitoCreate(HabitoBase):
    id_usuario: UUID


class HabitoUpdate(BaseModel):
    titulo: Optional[str]
    frecuencia: Optional[FrecuenciaEnum]
    activo: Optional[bool]
    id_categoria: Optional[UUID]


class HabitoOut(HabitoBase):
    id: UUID
    id_usuario: UUID
    fecha_creacion: date
