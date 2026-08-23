# models.py
# Modèle SQLAlchemy représentant la table "taches" en base de données

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TacheModel(Base):
    __tablename__ = "taches"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(String, index=True)
    date_echeance = Column(String, index=True)
    terminee = Column(Boolean, default=False)
    
