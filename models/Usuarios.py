from config.database import Base
from sqlalchemy import Column, Integer, String, Float


class Usuarios(Base):

    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key = True)
    nombre = Column(String(20))
    email = Column(String(50))
    password = Column(String(50))
    rol = Column(String(25))