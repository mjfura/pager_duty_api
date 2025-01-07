from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .env import DB_HOST,DB_NAME,DB_PASSWORD,DB_USER

# Crear la cadena de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crear el motor de base de datos
print('DB URL ',DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión
SessionLocal = sessionmaker(bind=engine)

# Base para modelos
Base = declarative_base()

db_session = SessionLocal()