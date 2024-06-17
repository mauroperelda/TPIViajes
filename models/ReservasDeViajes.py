from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Date


class ReservasDeViaje(Base):

    __tablename__ = "ReservasDeViaje"

    id = Column(Integer, primary_key=True)
    usuarioId = Column(Integer)
    paqueteId = Column(Integer)
    fecha_reserva = Column(Date)
    cantidad_personas = Column(Integer)

    