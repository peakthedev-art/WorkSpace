import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Docker fournit les variables DB_* à l'API ; les variables MYSQL_* restent
# acceptées pour le lancement local avec le fichier .env.
DB_USER = os.getenv("DB_USER") or os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME") or os.getenv("MYSQL_DATABASE")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError(
        "Variables manquantes : DB_USER, DB_PASSWORD, DB_NAME"
    )

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
