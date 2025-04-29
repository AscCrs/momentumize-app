from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.models.usuarios import UsuarioModel
from src.db.models.tareas import TareaModel
from src.db.models.categorias import CategoriaModel
from src.db.models.habitos import HabitoModel
from src.db.models.checkins import CheckinModel

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.habitos, document_models=[
        UsuarioModel, 
        TareaModel, 
        CategoriaModel, 
        HabitoModel,
        CheckinModel
    ])
