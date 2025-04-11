from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mps.config.db_config import CONNECTION_STRING

# Crear el motor de SQLAlchemy
engine = create_engine(CONNECTION_STRING)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
