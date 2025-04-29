from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
import uvicorn

from src.routes.usuarios import routes as usuario_routes
from src.routes.tareas import routes as tarea_routes
from src.routes.categorias import routes as categoria_routes
from src.routes.habitos import routes as habito_routes
from src.routes.checkins import routes as checkin_routes

from src.db.config.conn import init_db

app = Starlette(
    debug=True,
    routes=[
        Mount("/usuarios", routes=usuario_routes),
        Mount("/tareas", routes=tarea_routes),
        Mount("/categorias", routes=categoria_routes),
        Mount("/habitos", routes=habito_routes),
        Mount("/checkins", routes=checkin_routes),
    ],
)

# Middleware CORS (opcional si usas frontend separado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización Beanie con Motor
@app.on_event("startup")
async def startup_event():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
