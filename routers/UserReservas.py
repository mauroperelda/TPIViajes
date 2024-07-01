from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.ReservasDeViajes import ReservasDeViaje as ReservasDeViajeModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.ReservasDeViajesServices import ReservasDeViajeServices
from schemas.ReservasDeViajeSchemas import ReservasDeViajeSchema
from Security import auth

reservas_router = APIRouter()

@reservas_router.get('/ALL-RESERVAS', tags=['Reservas'])
def get_all_reservas():
    db = Session()
    reservas = ReservasDeViajeServices(db).get_all_reservas()
    if not reservas:
        return JSONResponse(status_code=404, content={"message": "No se encontro ninguna reserva"})
    return JSONResponse(status_code=200, content=jsonable_encoder(reservas))

@reservas_router.get('/ACT-RESERVA', tags=['Reservas'])
def get_act_reservas(user = Depends(auth.GetCurrentUser)):
    db = Session()
    reservas = ReservasDeViajeServices(db).get_act_reservas(user.id)
    if not reservas:
        return JSONResponse(status_code=404, content={"message": f"No se encontro ninguna reserva activa"})
    
    reservas_new = [
        {
            "id": reserva[0].id,
            "paqueteId": reserva[0].paqueteId,
            "nombre_paquete": reserva[1],
            "fecha_reserva": reserva[0].fecha_reserva,
            "cantidad_personas": reserva[0].cantidad_personas
        }
        for reserva in reservas
    ]
    return JSONResponse(status_code=200, content=jsonable_encoder(reservas_new))

@reservas_router.get('/total-reservas', tags=['Dashboard'])
def get_total_reservas():
    db = Session()
    total_reservas = ReservasDeViajeServices(db).get_total_reservas()
    return {"total_reservas": total_reservas}

@reservas_router.post('/RESERVAS', tags=['Reservas'])
def create_reservas(reserva: ReservasDeViajeSchema):
    db = Session()
    reservas = ReservasDeViajeServices(db).create_reservas(reserva)
    if not reservas:
        return JSONResponse(status_code=404, content={"message": "Reserva no creada"})
    return JSONResponse(status_code=200, content={"message": "Reserva creada con exito"})

@reservas_router.put('/RESERVAS', tags=['Reservas'])
def update_reservas(id: int, reserva):
    db = Session
    mod_reserva = ReservasDeViajeServices(db).update_reservas(id, reserva)
    if not mod_reserva:
        return JSONResponse(status_code=404, content={"message": "Reserva no modificada"})
    return JSONResponse(status_code=200, content={"message": "Reserva  modificada con exito"})

@reservas_router.delete('/RESERVAS', tags=['Reservas'])
def delete_reservas(id:int):
    db = Session()
    reserva = ReservasDeViajeServices(db).delete_reservas(id)
    if not reserva:
        return JSONResponse(status_code=404, content={"message": "Reserva no eliminada"})
    return JSONResponse(status_code=200, content={"message": "Reserva eliminada con exito"})


