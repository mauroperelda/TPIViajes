from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    #id: Optional[int] = None
    nombre: str = Field(min_length=2, max_length=20)
    email: EmailStr
    # password: str
    rol: str

class CreateUsuario(UsuarioBase):
    password: str

class UsuarioUpdate(UsuarioBase):
    password: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

#    class Config:
#        schema_extra = {
#            "example": {
#                "id": 1,
#                "nombre": "Elian",
#                "email": "elianmaineri@gmail.com",
#                "password": "Hola1234",
#                "rol": "Administrador | Cliente"
#            }
#        }

