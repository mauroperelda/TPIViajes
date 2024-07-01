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

@usuarios_router.get('/usuario-mas-reservas', tags=['Dashboard'])
def get_usuario_mas_reservas():
    db = Session()
    usuario_mas_reservas = UsuariosServices(db).get_usuario_mas_reservas()
    print(usuario_mas_reservas)  # Imprime el resultado de la consulta para debugging
    if usuario_mas_reservas:
        usuario_id, total_reservas = usuario_mas_reservas
        usuario = db.query(UsuariosModel).filter(UsuariosModel.id == usuario_id).first()
        if usuario:
            print(usuario)  # Imprime el usuario encontrado para debugging
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "usuario_id": usuario.id,
                "total_reservas": total_reservas,
                "nombre_usuario": usuario.nombre
            })
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No hay reservas"})

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
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
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
