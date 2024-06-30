from fastapi import APIRouter
from fastapi import Depends, Path, Query, status, Form
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.Usuarios import Usuarios as UsuariosModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.UsuariosServices import UsuariosServices
from schemas.UsuariosSchemas import UsuarioBase, CreateUsuario, UsuarioUpdate

usuarios_router = APIRouter()


@usuarios_router.get('/ALL-USUARIOS', tags=['Usuarios'], response_model=List[UsuarioBase])
def get_all_usuarios():
    db = Session()
    usuarios = UsuariosServices(db).get_all_usuarios()
    if not usuarios:
        return JSONResponse(status_code=404, content={"message": "No se encontro ningun usuario"})
    return JSONResponse(status_code=200, content=jsonable_encoder(usuarios))

@usuarios_router.get('/ID-USUARIOS', tags=['Usuarios'])
def get_id_usuarios(id: int):
    db = Session()
    usuarios = UsuariosServices(db).get_id_usuarios(id)
    if not usuarios:
        return JSONResponse(status_code=404, content={"message": "No se encontro ningun usuario con ese id"})
    return JSONResponse(status_code=200, content=jsonable_encoder(usuarios))

@usuarios_router.get('/EMAIL-USUARIOS', tags=['Usuarios'])
def get_email_usuarios(email: str):
    db = Session()
    usuarios = UsuariosServices(db).get_id_usuarios(email)
    if not usuarios:
        return JSONResponse(status_code=404, content={"message": "No se encontro ningun usuario con ese email"})
    return JSONResponse(status_code=200, content=jsonable_encoder(usuarios))

@usuarios_router.post('/USUARIOS', tags=['Usuarios'], response_model=UsuarioBase, status_code=status.HTTP_201_CREATED)
def create_usuarios(nombre: str = Form(...), email: str = Form(...), password: str = Form(...), rol: str = Form(...)):
    db = Session()
    usuario = CreateUsuario(nombre= nombre, email = email, password = password, rol = rol)
    usuarios = UsuariosServices(db).create_usuarios(usuario)
    if not usuarios:
        return JSONResponse(status_code=500, content={"message": "Usuario no creado"})
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    # return JSONResponse(status_code=200, content={"message": "Usuario creado con exito"})

@usuarios_router.put('/USUARIOS', tags=['Usuarios'])
def update_usuarios(id: int, usuario: UsuarioUpdate):
    db = Session()
    usuarios = UsuariosServices(db).update_usuarios(id, usuario)
    if not usuarios:
        return JSONResponse(status_code=500, content={"message": "Usuario no modificado"})
    return JSONResponse(status_code=200, content={"message": "Usuario modificado con exito"})

@usuarios_router.delete('/USUARIOS', tags=['Usuarios'])
def delete_usuarios(id: int):
    db = Session()
    usuarios = UsuariosServices(db).delete_usuarios(id)
    if not usuarios:
        return JSONResponse(status_code=500, content={"message": "Usuario no eliminado"})
    return JSONResponse(status_code=200, content={"message": "Usuario eliminado con exito"})
