from fastapi import APIRouter
from fastapi import Depends, Path, Query
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

@paquetes_router.get('/DESTINO-PAQUETE', tags=['Paquete'], response_model=PaquetesDeViaje, status_code=200, dependencies=[Depends(JWTBearer())])
def get_destino_paquete(destino:str):
    db = Session()
    paquete = PaqueteDeViajesServices(db).get_destino_paqueteDeViaje(destino)
    if not paquete:
        return JSONResponse(status_code=404, content={"message": "Paquete de viaje con ese destino NO ENCONTRADO"})
    return JSONResponse(status_code=200, content=jsonable_encoder(paquete))
