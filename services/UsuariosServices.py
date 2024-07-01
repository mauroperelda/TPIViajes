from models.Usuarios import Usuarios as UsuariosModel
from schemas.UsuariosSchemas import UsuarioBase, CreateUsuario, UsuarioUpdate
from Security.auth import GetPasswordHash


class UsuariosServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_usuarios(self):
        usuarios = self.db.query(UsuariosModel).all()
        return usuarios
    
    def get_id_usuarios(self, id: int):
        usuarios = self.db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        return usuarios
    
    def get_email_usuarios(self, email: str):
        usuarios = self.db.query(UsuariosModel).filter(UsuariosModel.email == email).first()
        return usuarios
    
    def get_usuario_mas_reservas(self):
        usuario_mas_reservas = (db.query(ReservasDeViajeModel.usuarioId, func.count(ReservasDeViajeModel.id).label('total'))
            .group_by(ReservasDeViajeModel.usuarioId)
            .order_by(func.count(ReservasDeViajeModel.id).desc())
            .first())
        return usuario_mas_reservas
    
    def create_usuarios(self, usuario: CreateUsuario):
        hashed_password = GetPasswordHash(usuario.password)
        new_usuario = UsuariosModel(
            nombre= usuario.nombre,
            email = usuario.email,
            password = hashed_password,
            rol = usuario.rol
        )
        self.db.add(new_usuario)
        self.db.commit()
        return new_usuario
    
    def update_usuarios(self, id: int, data: UsuarioUpdate):
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        usuario.nombre = data.nombre
        usuario.email = data.email
        usuario.password = data.password
        usuario.rol = data.rol
        self.db.commit()
        return usuario
    
    def delete_usuarios(self, id: int):
        self.db.query(UsuariosModel).filter(UsuariosModel.id == id).delete()
        self.db.commit()
        return
    