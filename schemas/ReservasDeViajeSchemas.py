from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ReservasDeViajeSchema(BaseModel):

    id: int
    usuarioId: int
    paqueteId: int
    fecha_reserva: date
    cantidad_personas: int

