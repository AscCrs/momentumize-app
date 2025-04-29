from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from uuid import UUID, uuid4
from datetime import date

from src.db.models.tareas import TareaModel
from src.db.schemas.tarea import TareaCreate, TareaUpdate

# Crear tarea
async def crear_tarea(request: Request):
    try:
        data = await request.json()
        tarea_data = TareaCreate(**data)

        nueva_tarea = TareaModel(
            id=uuid4(),
            id_usuario=tarea_data.id_usuario,
            descripcion=tarea_data.descripcion,
            fecha_limite=tarea_data.fecha_limite,
            completada=False,
            fecha_creacion=date.today()
        )
        await nueva_tarea.insert()
        return JSONResponse(content={"id": str(nueva_tarea.id)}, status_code=201)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Obtener todas las tareas
async def listar_tareas(request: Request):
    tareas = await TareaModel.find_all().to_list()
    resultado = [
        {
            "id": str(t.id),
            "id_usuario": str(t.id_usuario),
            "descripcion": t.descripcion,
            "fecha_limite": t.fecha_limite.isoformat() if t.fecha_limite else None,
            "completada": t.completada,
            "fecha_creacion": t.fecha_creacion.isoformat()
        }
        for t in tareas
    ]
    return JSONResponse(content=resultado, status_code=200)

# Obtener tareas por usuario
async def listar_tareas_por_usuario(request: Request):
    try: 
        id_usuario = request.path_params["id_usuario"]
        tareas = await TareaModel.find(TareaModel.id_usuario == UUID(id_usuario)).to_list()
        resultado = [
            {
                "id": str(t.id),
                "id_usuario": str(t.id_usuario),
                "descripcion": t.descripcion,
                "fecha_limite": t.fecha_limite.isoformat() if t.fecha_limite else None,
                "completada": t.completada,
                "fecha_creacion": t.fecha_creacion.isoformat()
            }
            for t in tareas
        ]
        return JSONResponse(content=resultado)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


# Obtener tarea por ID
async def obtener_tarea(request: Request):
    id_tarea = request.path_params["id"]
    tarea = await TareaModel.get(UUID(id_tarea))
    if tarea:
        return JSONResponse(content={
            "id": str(tarea.id),
            "id_usuario": str(tarea.id_usuario),
            "descripcion": tarea.descripcion,
            "fecha_limite": tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
            "completada": tarea.completada,
            "fecha_creacion": tarea.fecha_creacion.isoformat()
        })
    return JSONResponse(content={"error": "Tarea no encontrada"}, status_code=404)

# Actualizar tarea
async def actualizar_tarea(request: Request):
    id_tarea = request.path_params["id"]
    tarea = await TareaModel.get(UUID(id_tarea))
    if not tarea:
        return JSONResponse(content={"error": "Tarea no encontrada"}, status_code=404)

    try:
        data = await request.json()
        update_data = TareaUpdate(**data)

        if update_data.descripcion is not None:
            tarea.descripcion = update_data.descripcion
        if update_data.fecha_limite is not None:
            tarea.fecha_limite = update_data.fecha_limite
        if update_data.completada is not None:
            tarea.completada = update_data.completada

        await tarea.save()
        return JSONResponse(content={"mensaje": "Tarea actualizada"})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Eliminar tarea
async def eliminar_tarea(request: Request):
    id_tarea = request.path_params["id"]
    tarea = await TareaModel.get(UUID(id_tarea))
    if not tarea:
        return JSONResponse(content={"error": "Tarea no encontrada"}, status_code=404)
    
    await tarea.delete()
    return JSONResponse(content={"mensaje": "Tarea eliminada"})

# Rutas del router
routes = [
    Route("/", crear_tarea, methods=["POST"]),
    Route("/all", listar_tareas, methods=["GET"]),
    Route("/usuario/{id_usuario}", listar_tareas_por_usuario, methods=["GET"]),
    Route("/{id}", obtener_tarea, methods=["GET"]),
    Route("/{id}", actualizar_tarea, methods=["PUT"]),
    Route("/{id}", eliminar_tarea, methods=["DELETE"]),
]
