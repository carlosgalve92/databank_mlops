from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Cargar variables desde el entorno o .env
username = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "postgres")
host = os.getenv("DB_HOST", "postgres2")
port = os.getenv("DB_PORT", "15432")
database = os.getenv("DB_NAME", "postgres")

# Crear objeto URL sin exponer credenciales directamente en la cadena
url_object = URL.create(
    drivername="postgresql+psycopg2",  # Especificamos el driver
    username=None,  # No usamos username directamente en la URL
    password=None,  # No usamos password directamente en la URL
    host=host,  # Se pasa en la URL
    port=port,  # Se pasa en la URL
    database=database,  # Se pasa en la URL
)

# Crear engine de forma segura
engine = create_engine(
    url_object,
    connect_args={
        "user": username,  # Credenciales pasadas por connect_args
        "password": password,  # Credenciales pasadas por connect_args
        # "sslmode": "require"
    },
    pool_pre_ping=True,  # Mejora la estabilidad de la conexión en producción
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print("Database transaction failed:", e)
        raise
    finally:
        db.close()
