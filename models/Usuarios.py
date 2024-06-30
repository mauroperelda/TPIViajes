from config.database import Base
from sqlalchemy import Column, Integer, String, Float


class Usuarios(Base):

    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key = True, index=True)
    nombre = Column(String(20))
    email = Column(String(50), unique=True)
    password = Column(String(500))
    rol = Column(String(25))