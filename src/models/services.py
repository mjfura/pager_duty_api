from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.config import Base

class Service(Base):
    __tablename__ = "services"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(50), unique=True, nullable=False)  # ID de la API
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    incidents = relationship("Incident", back_populates="service")
    teams = relationship("ServiceTeam", back_populates="service")
    escalation_policies = relationship("ServiceEscalationPolicy", back_populates="service")