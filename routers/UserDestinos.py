from fastapi import APIRouter
from fastapi import Depends, Path, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.Destinos import Destinos as DestinosModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.DestinosServices import DestinosServices
from schemas.DestinosSchemas import Destinos

destinos_router = APIRouter()

@destinos_router.get('/ALL-DESTINOS', tags=['Destinos'], status_code=status.HTTP_200_OK)
def get_all_destinos():
    db = Session()
    try:
        destinos = DestinosServices(db).get_all_destinos()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(destinos))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontro ningun destino"})

@destinos_router.get('/search-destinos', tags=['Destinos'], status_code=status.HTTP_200_OK)
def search_destinos(query: str):
    db = Session()
    try:
        destinos_nombre = DestinosServices(db).get_nombre_destinos(query)
        destinos_pais = DestinosServices(db).get_pais_destinos(query)
        
        destinos = []
        if destinos_nombre:
            destinos.append(destinos_nombre)
        if destinos_pais and destinos_pais not in destinos:
            destinos.append(destinos_pais)

        if not destinos:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontraron destinos"})
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(destinos))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
# @destinos_router.get('/NOMBRE-DESTINOS', tags=['Destinos'], response_model=Destinos, status_code=200, dependencies=[Depends(JWTBearer())])
# def get_nom_destinos(nombre:str):
#     db = Session()
#     destinos = DestinosServices(db).get_nombre_destinos(nombre)
#     if not destinos:
#         return JSONResponse(status_code=404, content={"message": "Nombre de destino no encontrado"})
#     return JSONResponse(status_code=200, content=jsonable_encoder(destinos))

# @destinos_router.get('/PAIS-DESTINOS', tags=['Destinos'], response_model=Destinos, status_code=200, dependencies=[Depends(JWTBearer())])
# def get_pais_destinos(pais:str):
#     db = Session()
#     destinos = DestinosServices(db).get_pais_destinos(pais)
#     if not destinos:
#         return JSONResponse(status_code=404, content={"message": "Destinos de ese pais no encontrados"})
#     return JSONResponse(status_code=200, content=jsonable_encoder(destinos))


@destinos_router.post('/DESTINOS_CREATE', tags=['Destinos'], response_model=Destinos, status_code=200)
def create_destinos(destino: Destinos):
    db = Session()
    new_destino = DestinosServices(db).create_destinos(destino)
    if not new_destino:
        return JSONResponse(status_code=500, content={"message": "Destino no creado"})
    return JSONResponse(status_code=200, content={"message": "Destino creado con exito"})

@destinos_router.put('/DESTINOS', tags=['Destinos'], response_model=Destinos, status_code=200)
def update_destinos(id: int, destino):
    db = Session()
    mod_destino = DestinosServices(db).update_destinos(destino)
    if not mod_destino:
        return JSONResponse(status_code=500, content={"message": "Destino no modificado"})
    return JSONResponse(status_code=200, content={"message": "Destino modificado con exito"})

@destinos_router.delete('/DESTINOS', tags=['Destinos'], response_model=Destinos, status_code=200)
def delete_destinos(id: int):
    db = Session()
    del_destino = DestinosServices(db).delete_destinos(id)
    if not del_destino:
        return JSONResponse(status_code=500, content={"message": "Destino no eliminado"})
    return JSONResponse(status_code=200, content={"message": "Destino eliminado con exito"})


