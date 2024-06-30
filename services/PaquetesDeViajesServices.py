from models.PaquetesDeViajes import PaquetesDeViajes as PaquetesDeViajeModel
from schemas.PaquetesDeViajesSchemas import PaquetesDeViaje
 


class PaqueteDeViajesServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_paquetes(self):
        paquetes = self.db.query(PaquetesDeViajeModel).all()
        return paquetes

    def get_destino_paqueteDeViaje(self, destinoId: int):
        paqueteDeViaje = self.db.query(PaquetesDeViajeModel).filter(PaquetesDeViajeModel.destinoId == destinoId).first()
        return paqueteDeViaje
    
    def create_paquete(self, paquete: PaquetesDeViaje):
        new_paquete = PaquetesDeViajeModel(**paquete.dict())
        self.db.add(new_paquete)
        self.db.commit()
        return new_paquete
    
    def update_paquete(self, id: int, data: PaquetesDeViaje):
        paquete = self.db.query(PaquetesDeViajeModel).filter(PaquetesDeViajeModel.id == id).first()
        paquete.destinoId = data.destinoId
        paquete.nombre = data.nombre
        paquete.precio = data.precio
        paquete.cupo = data.cupo
        paquete.fecha_inicio = data.fecha_inicio
        paquete.fecha_fin = data.fecha_fin
        self.db.commit()
        return paquete
    
    def delete_paquete(self, id: int):
        self.db.query(PaquetesDeViajeModel).filter(PaquetesDeViajeModel.id == id).delete()
        self.db.commit()
        return
