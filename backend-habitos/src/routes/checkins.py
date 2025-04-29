from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from uuid import UUID, uuid4
from datetime import date

from src.db.models.checkins import CheckinModel
from src.db.schemas.checkin import CheckinCreate, CheckinOut, CheckinUpdate
from src.db.models.habitos import HabitoModel

# Crear un nuevo checkin
async def crear_checkin(request: Request):
    try:
        data = await request.json()
        checkin_data = CheckinCreate(**data)
        
        if not data.get("fecha"):
            checkin_data.fecha = date.today()
        else:
            checkin_data.fecha = date.fromisoformat(data["fecha"])

        nuevo_checkin = CheckinModel(
            id=uuid4(),
            id_habito=checkin_data.id_habito,
            fecha=checkin_data.fecha,
            completado=checkin_data.completado
        )
        await nuevo_checkin.insert()
        return JSONResponse(content={"id": str(nuevo_checkin.id)}, status_code=201)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


# Obtener todos los checkins
async def listar_checkins(request: Request):
    checkins = await CheckinModel.find_all().to_list()
    resultado = [
        {
            "id": str(c.id),
            "id_habito": str(c.id_habito),
            "fecha": c.fecha.isoformat(),
            "completado": c.completado
        }
        for c in checkins
    ]
    return JSONResponse(content=resultado)

# Obtener checkin por habito
async def listar_checkins_por_habito(request: Request):
    try: 
        id_habito = request.path_params["id_habito"]
        checkins = await CheckinModel.find(CheckinModel.id_habito == UUID(id_habito)).to_list()
        habito = await HabitoModel.get(UUID(id_habito))
        
        resultado = [
            {
                "id": str(c.id),
                "id_habito": str(c.id_habito),
                "nombre_habito": str(habito.titulo),
                "fecha": c.fecha.isoformat(),
                "completado": c.completado
            }
            for c in checkins
        ]
        return JSONResponse(content=resultado)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


# Obtener un checkin por ID
async def obtener_checkin(request: Request):
    id_checkin = request.path_params["id"]
    checkin = await CheckinModel.get(UUID(id_checkin))
    if checkin:
        return JSONResponse(content={
            "id": str(checkin.id),
            "id_habito": str(checkin.id_habito),
            "fecha": checkin.fecha.isoformat(),
            "completado": checkin.completado
        })
    return JSONResponse(content={"error": "Checkin no encontrado"}, status_code=404)


# Actualizar un checkin
async def actualizar_checkin(request: Request):
    id_checkin = request.path_params["id"]
    checkin = await CheckinModel.get(UUID(id_checkin))
    if not checkin:
        return JSONResponse(content={"error": "Checkin no encontrado"}, status_code=404)

    data = await request.json()
    update_data = CheckinUpdate(**data)

    if update_data.completado is not None:
        checkin.completado = update_data.completado

    await checkin.save()
    return JSONResponse(content={"mensaje": "Checkin actualizado"})


# Eliminar un checkin
async def eliminar_checkin(request: Request):
    id_checkin = request.path_params["id"]
    checkin = await CheckinModel.get(UUID(id_checkin))
    if not checkin:
        return JSONResponse(content={"error": "Checkin no encontrado"}, status_code=404)

    await checkin.delete()
    return JSONResponse(content={"mensaje": "Checkin eliminado"})


# Registrar rutas
routes = [
    Route("/", crear_checkin, methods=["POST"]),
    Route("/all", listar_checkins, methods=["GET"]),
    Route("/{id}", obtener_checkin, methods=["GET"]),
    Route("/habito/{id_habito}", listar_checkins_por_habito, methods=["GET"]),
    Route("/{id}", actualizar_checkin, methods=["PUT"]),
    Route("/{id}", eliminar_checkin, methods=["DELETE"]),
]
