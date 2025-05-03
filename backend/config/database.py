# config/database.py
# Configuración de la base de datos con SQLAlchemy para Cuentix

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ruta a la base de datos SQLite (local por ahora)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'cuentix.db')
DB_URL = f"sqlite:///{DB_PATH}"

# Crear motor de conexión
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# Crear sesión de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()
