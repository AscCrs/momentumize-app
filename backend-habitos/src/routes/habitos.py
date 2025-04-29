from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status
from uuid import UUID, uuid4
from datetime import date

from src.db.models.habitos import HabitoModel
from src.db.schemas.habito import HabitoCreate, HabitoUpdate
from src.db.models.usuarios import UsuarioModel
from src.db.models.categorias import CategoriaModel

# Crear un nuevo hábito
async def crear_habito(request: Request):
    try:
        data = await request.json()
        habito_data = HabitoCreate(**data)

        nuevo_habito = HabitoModel(
            id=uuid4(),
            id_usuario=habito_data.id_usuario,
            id_categoria=habito_data.id_categoria,
            titulo=habito_data.titulo,
            frecuencia=habito_data.frecuencia,
            activo=habito_data.activo,
            fecha_creacion=date.today()
        )
        await nuevo_habito.insert()
        return JSONResponse(content={"id": str(nuevo_habito.id)}, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


# Listar todos los hábitos
async def listar_habitos(request: Request):
    try:
        habitos = await HabitoModel.find_all().to_list()
        resultado = [
            {
                "id": str(h.id),
                "id_usuario": str(h.id_usuario),
                "id_categoria": str(h.id_categoria) if h.id_categoria else None,
                "titulo": h.titulo,
                "frecuencia": h.frecuencia,
                "activo": h.activo,
                "fecha_creacion": h.fecha_creacion.isoformat()
            }
            for h in habitos
        ]
        return JSONResponse(content=resultado, status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Listar habitos por categoria
async def listar_habitos_por_categoria(request: Request):
    try:
        id_categoria = request.path_params["id_categoria"]
        habitos = await HabitoModel.find(HabitoModel.id_categoria == UUID(id_categoria)).to_list()
        cat = await CategoriaModel.get(UUID(id_categoria))
        usuario = await UsuarioModel.get(habitos[0].id_usuario) if habitos else None
        
        resultado = [
            {
                "id": str(h.id),
                "usuario": {
                    "id_usuario": str(usuario.id) if usuario else None,
                    "nombre_usuario": str(usuario.nombre) if usuario else None,
                },
                "categoria": {
                  "id_categoria": str(h.id_categoria) if h.id_categoria else None,
                  "nombre_categoria": str(cat.nombre) if cat else None,  
                },
                "titulo": h.titulo,
                "frecuencia": h.frecuencia,
                "activo": h.activo,
                "fecha_creacion": h.fecha_creacion.isoformat()
            }
            for h in habitos
        ]
        return JSONResponse(content=resultado, status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Obtener un hábito por ID
async def obtener_habito(request: Request):
    try:
        id_habito = request.path_params["id"]
        habito = await HabitoModel.get(UUID(id_habito))
        if habito:
            # Obtener el usuario y la categoría del hábito
            usuario = await UsuarioModel.get(habito.id_usuario)
            cat = await CategoriaModel.get(habito.id_categoria) if habito.id_categoria else None
            
            return JSONResponse(content={
                "id": str(habito.id),
                "usuario": {
                    "id_usuario": str(usuario.id) if usuario else None,
                    "nombre_usuario": str(usuario.nombre) if usuario else None,
                },
                "categoria": {
                  "id_categoria": str(habito.id_categoria) if habito.id_categoria else None,
                  "nombre_categoria": str(cat.nombre) if cat else None,  
                },
                "titulo": habito.titulo,
                "frecuencia": habito.frecuencia,
                "activo": habito.activo,
                "fecha_creacion": habito.fecha_creacion.isoformat()
            }, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"error": "Hábito no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


# Actualizar un hábito
async def actualizar_habito(request: Request):
    try:
        id_habito = request.path_params["id"]
        habito = await HabitoModel.get(UUID(id_habito))
        if not habito:
            return JSONResponse(content={"error": "Hábito no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

        data = await request.json()
        update_data = HabitoUpdate(**data)

        if update_data.titulo is not None:
            habito.titulo = update_data.titulo
        if update_data.frecuencia is not None:
            habito.frecuencia = update_data.frecuencia
        if update_data.activo is not None:
            habito.activo = update_data.activo
        if update_data.id_categoria is not None:
            habito.id_categoria = update_data.id_categoria

        await habito.save()
        return JSONResponse(content={"mensaje": "Hábito actualizado"}, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


# Eliminar un hábito
async def eliminar_habito(request: Request):
    try:
        id_habito = request.path_params["id"]
        habito = await HabitoModel.get(UUID(id_habito))
        if not habito:
            return JSONResponse(content={"error": "Hábito no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

        await habito.delete()
        return JSONResponse(content={"mensaje": "Hábito eliminado"}, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

routes = [
    Route("/", crear_habito, methods=["POST"]),
    Route("/all", listar_habitos, methods=["GET"]),
    Route("/categoria/{id_categoria}", listar_habitos_por_categoria, methods=["GET"]),
    Route("/{id}", obtener_habito, methods=["GET"]),
    Route("/{id}", actualizar_habito, methods=["PUT"]),
    Route("/{id}", eliminar_habito, methods=["DELETE"]),
]
