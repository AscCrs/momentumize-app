from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from uuid import UUID, uuid4
from datetime import date

from src.db.models.usuarios import UsuarioModel
from src.db.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate

# Crear usuario
async def crear_usuario(request: Request):
    try: 
        data = await request.json()
        usuario_data = UsuarioCreate(**data)

        nuevo_usuario = UsuarioModel(
            id=uuid4(),
            nombre=usuario_data.nombre,
            correo=usuario_data.correo,
            fecha_registro=date.today()
        )
        await nuevo_usuario.insert()
        return JSONResponse(content={"id": str(nuevo_usuario.id)}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Obtener todos
async def listar_usuarios(request: Request):
    try:
        usuarios = await UsuarioModel.find_all().to_list()
        resultado = [
            {
                "id": str(u.id),
                "nombre": u.nombre,
                "correo": u.correo,
                "fecha_registro": u.fecha_registro.isoformat()
            }
            for u in usuarios
        ]
        return JSONResponse(content=resultado, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Obtener por ID
async def obtener_usuario(request: Request):
    id_usuario = request.path_params["id"]
    usuario = await UsuarioModel.get(UUID(id_usuario))
    if usuario:
        return JSONResponse(content={
            "id": str(usuario.id),
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "fecha_registro": usuario.fecha_registro.isoformat()
        }, status_code=200)
    return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

# Actualizar usuario
async def actualizar_usuario(request: Request):
    id_usuario = request.path_params["id"]
    usuario = await UsuarioModel.get(UUID(id_usuario))
    if not usuario:
        return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

    data = await request.json()
    update_data = UsuarioUpdate(**data)

    if update_data.nombre:
        usuario.nombre = update_data.nombre
    if update_data.correo:
        usuario.correo = update_data.correo

    await usuario.save()
    return JSONResponse(content={"mensaje": "Usuario actualizado"})

# Eliminar usuario
async def eliminar_usuario(request: Request):
    id_usuario = request.path_params["id"]
    usuario = await UsuarioModel.get(UUID(id_usuario))
    if not usuario:
        return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)
    
    await usuario.delete()
    return JSONResponse(content={"mensaje": "Usuario eliminado"}, status_code=200)

# Rutas
routes = [
    Route("/", crear_usuario, methods=["POST"]),
    Route("/all", listar_usuarios, methods=["GET"]),
    Route("/{id}", obtener_usuario, methods=["GET"]),
    Route("/{id}", actualizar_usuario, methods=["PUT"]),
    Route("/{id}", eliminar_usuario, methods=["DELETE"]),
]
