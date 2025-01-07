from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.config import Base

class Team(Base):
    __tablename__ = "teams"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String(50), unique=True, nullable=False)  # ID de la API
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    services = relationship("ServiceTeam", back_populates="team")
    incidents = relationship("IncidentTeam", back_populates="team")
    escalation_policies = relationship("TeamEscalationPolicy", back_populates="team")