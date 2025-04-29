from beanie import Document
from uuid import UUID
from datetime import date
from pydantic import Field


class CheckinModel(Document):
    id: UUID = Field(default_factory=UUID, alias="_id")
    id_habito: UUID
    fecha: date
    completado: bool

    class Settings:
        name = "checkins"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
