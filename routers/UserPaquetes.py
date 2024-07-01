from fastapi import APIRouter
from fastapi import Depends, Path, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.PaquetesDeViajes import PaquetesDeViajes as PaquetesDeViajesModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.PaquetesDeViajesServices import PaqueteDeViajesServices
from schemas.PaquetesDeViajesSchemas import PaquetesDeViaje

paquetes_router = APIRouter()


@paquetes_router.get('/ALL-PAQUETES', tags=['Paquetes'])
def get_all_paquetes():
    db = Session()
    paquetes = PaqueteDeViajesServices(db).get_all_paquetes()
    if not paquetes:
        return JSONResponse(status_code=404, content={"message": "Paquetes no encontrados"})
    return JSONResponse(status_code=200, content=jsonable_encoder(paquetes))

@paquetes_router.get('/DESTINO-PAQUETE', tags=['Paquetes'], status_code=200)
def get_destino_paquete(destino: str):
    db = Session()
    paquete = PaqueteDeViajesServices(db).get_destino_paqueteDeViaje(destino)
    if not paquete:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Paquete de viaje con ese destino NO ENCONTRADO"})
    return JSONResponse(status_code=200, content=jsonable_encoder(paquete))

@paquetes_router.post('/PAQUETES', tags=['Paquetes'])
def create_paquetes(paquete: PaquetesDeViaje):
    db = Session()
    paquetes = PaqueteDeViajesServices(db).create_paquete(paquete)
    if not paquete:
        return JSONResponse(status_code=500, content={"message": "Paquete no creeado"})
    return JSONResponse(status_code=200, content={"message": "Paquete creado con exito"})

@paquetes_router.get('/paquete-mas-reservado', tags=['Dashboard'])
def get_paquete_mas_reservado():
    db = Session()
    paquete_mas_reservado = PaqueteDeViajesServices(db).get_paquete_mas_reservado()
    if paquete_mas_reservado:
        paquete = db.query(PaquetesDeViajesModel).filter(PaquetesDeViajesModel.id == paquete_mas_reservado[0]).first()
        return {"paquete_id": paquete.id, "total_reservas": paquete_mas_reservado.total, "nombre_paquete": paquete.nombre}
    return {"message": "No hay reservas"}

@paquetes_router.put('/PAQUETES', tags=['Paquetes'])
def update_paquetes(id: int, paquete):
    db = Session()
    paquetes = PaqueteDeViajesServices(db).update_paquete(id, paquete)
    if not paquete:
        return JSONResponse(status_code=500, content={"message": "Paquete no modificado"})
    return JSONResponse(status_code=200, content={"message": "Paquete modificado con exito"})

@paquetes_router.delete('/PAQUETES', tags=['Paquetes'])
def delete_paquetes(id:int):
    db = Session()
    paquetes = PaqueteDeViajesServices(db).delete_paquete(id)
    if not paquetes:
        return JSONResponse(status_code=500, content={"message": "Paquete no eliminado"})
    return JSONResponse(status_code=200, content={"message": "Paquete eliminado con exito"})



    



