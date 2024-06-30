from models.Destinos import Destinos as DestinosModel
from schemas.DestinosSchemas import Destinos 
from typing import Optional, List


class DestinosServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_destinos(self):
        try:
            destinos = self.db.query(DestinosModel).all()
            return destinos
        except Exception as e:
            print(f"Error: {e}")
            return[]
    
    def get_nombre_destinos(self, nombre):
        destinos = self.db.query(DestinosModel).filter(DestinosModel.nombre == nombre).first()
        return destinos
    
    def get_pais_destinos(self, pais):
        destinos = self.db.query(DestinosModel).filter(DestinosModel.pais == pais).first()
        return destinos
    
    def create_destinos(self, destino: Destinos):
        new_destino = DestinosModel(**destino.dict())
        self.db.add(new_destino)
        self.db.commit()
        return new_destino
    
    def update_destinos(self, id: int, data: Destinos):
        destinos = self.db.query(DestinosModel).filter(DestinosModel.id == id).first()
        destinos.nombre = data.nombre
        destinos.descripcion = data.descripcion
        destinos.pais = data.pais
        self.db.commit()
        return destinos
    
    def delete_destinos(self, id: int):
        self.db.query(DestinosModel).filter(DestinosModel.id == id).delete()
        self.db.commit()
        return
    