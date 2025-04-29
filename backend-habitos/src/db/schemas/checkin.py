from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional


class CheckinCreate(BaseModel):
    id_habito: UUID
    fecha: date
    completado: bool

class CheckinUpdate(BaseModel):
    completado: Optional[bool] = None

class CheckinOut(BaseModel):
    id: UUID
    id_habito: UUID
    fecha: date
    completado: bool