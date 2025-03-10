import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno desde .env
load_dotenv()

# 🔹 URL de la base de datos (debe coincidir con docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://showroom_user:password@postgres:5432/showroom_db")

# 🔹 Crear conexión con PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔹 Dependencia de sesión para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
