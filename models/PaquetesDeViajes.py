from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class PaquetesDeViajes(Base):

    __tablename__ = "PaquetesDeViajes"

    id = Column(Integer,  primary_key=True, index=True)
    destinoId = Column(Integer, ForeignKey('Destinos.id'))
    nombre = Column(String(30))
    precio = Column(Float)
    cupo = Column(Integer)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    destino = relationship("Destinos")
    