from pydantic import BaseModel, Field
from typing import Optional


class Destinos(BaseModel):
    id: int
    nombre: str
    descripcion: str
    pais: str

