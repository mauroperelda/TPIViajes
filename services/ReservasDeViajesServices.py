from models.ReservasDeViajes import ReservasDeViaje as ReservasDeViajeModel
from schemas.ReservasDeViajeSchemas import ReservasDeViajeSchema


class ReservasDeViajeServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_all_reservas(self):
        reservas = self.db.query(ReservasDeViajeModel).all()
        return reservas

    def get_act_reservas(self, id):
        reservasAct = self.db.query(ReservasDeViajeModel).filter(ReservasDeViajeModel.usuarioId == id).first()
        return reservasAct

    def create_reservas(self, reserva: ReservasDeViajeSchema):
        new_reserva = ReservasDeViajeModel(**reserva.dict())
        self.db.add(new_reserva)
        self.db.commit()
        return
    
    def update_reservas(self, id: int, data: ReservasDeViajeSchema):
        reserva = self.db.query(ReservasDeViajeModel).filter(ReservasDeViajeModel.id == id).first()
        reserva.usuarioId = data.usuarioId
        reserva.paqueteId = data.paqueteId
        reserva.fecha_reserva = data.fecha_reserva
        reserva.cantidad_personas = data.cantidad_personas
        self.db.commit()
        return
    
    def delete_reservas(self, id: int):
        self.db.query(ReservasDeViajeModel).filter(ReservasDeViajeModel.id == id).delete()
        self.db.commit()
        return
