from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status
from uuid import UUID, uuid4

from src.db.models.categorias import CategoriaModel
from src.db.schemas.categoria import CategoriaCreate, CategoriaUpdate

# Crear una categoría
async def crear_categoria(request: Request):
    try:
        data = await request.json()
        categoria_data = CategoriaCreate(**data)

        nueva_categoria = CategoriaModel(
            id=uuid4(),
            nombre=categoria_data.nombre,
            descripcion=categoria_data.descripcion
        )
        await nueva_categoria.insert()

        return JSONResponse(
            content={"id": str(nueva_categoria.id)},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Listar todas las categorías
async def listar_categorias(request: Request):
    try:
        categorias = await CategoriaModel.find_all().to_list()
        resultado = [
            {
                "id": str(c.id),
                "nombre": c.nombre,
                "descripcion": c.descripcion
            }
            for c in categorias
        ]
        return JSONResponse(content=resultado, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Obtener una categoría por ID
async def obtener_categoria(request: Request):
    try:
        id_categoria = request.path_params["id"]
        categoria = await CategoriaModel.get(UUID(id_categoria))
        if categoria:
            return JSONResponse(
                content={
                    "id": str(categoria.id),
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion
                },
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"error": "Categoría no encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Actualizar una categoría
async def actualizar_categoria(request: Request):
    try:
        id_categoria = request.path_params["id"]
        categoria = await CategoriaModel.get(UUID(id_categoria))
        if not categoria:
            return JSONResponse(content={"error": "Categoría no encontrada"}, status_code=status.HTTP_404_NOT_FOUND)

        data = await request.json()
        update_data = CategoriaUpdate(**data)

        if update_data.nombre:
            categoria.nombre = update_data.nombre
        if update_data.descripcion is not None:
            categoria.descripcion = update_data.descripcion

        await categoria.save()

        return JSONResponse(content={"mensaje": "Categoría actualizada"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Eliminar una categoría
async def eliminar_categoria(request: Request):
    try:
        id_categoria = request.path_params["id"]
        categoria = await CategoriaModel.get(UUID(id_categoria))
        if not categoria:
            return JSONResponse(content={"error": "Categoría no encontrada"}, status_code=status.HTTP_404_NOT_FOUND)
        
        await categoria.delete()

        return JSONResponse(content={"mensaje": "Categoría eliminada"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

# Rutas
routes = [
    Route("/", crear_categoria, methods=["POST"]),
    Route("/all", listar_categorias, methods=["GET"]),
    Route("/{id}", obtener_categoria, methods=["GET"]),
    Route("/{id}", actualizar_categoria, methods=["PUT"]),
    Route("/{id}", eliminar_categoria, methods=["DELETE"]),
]
