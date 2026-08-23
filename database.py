from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///./test.db"  # Replace with your database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()   

# Fonction de dépendance : fournit une session DB fraîche à chaque requête,
# et garantit sa fermeture après usage (même en cas d'erreur)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()