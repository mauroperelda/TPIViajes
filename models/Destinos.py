from config.database import Base
from sqlalchemy import Column, String, Integer, Float


class Destinos(Base):

    __tablename__ = "Destinos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    descripcion = Column(String(70))
    pais = Column(String(30))
