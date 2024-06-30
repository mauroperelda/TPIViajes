from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class ReservasDeViaje(Base):

    __tablename__ = "ReservasDeViaje"

    id = Column(Integer, primary_key=True, index=True)
    usuarioId = Column(Integer, ForeignKey('Usuarios.id'))
    paqueteId = Column(Integer, ForeignKey('PaquetesDeViajes.id'))
    fecha_reserva = Column(Date)
    cantidad_personas = Column(Integer)
    usuario = relationship("Usuarios")
    paquete = relationship("PaquetesDeViajes")

    