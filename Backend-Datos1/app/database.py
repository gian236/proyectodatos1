# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Crear una instancia de Base
Base = declarative_base()

# Configura la URL de tu base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://proyectodatos:proyectodatos123@localhost:5436/proyectodatos"

# Crea el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
