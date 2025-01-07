from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.config import Base

class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(50), unique=True, nullable=False)  # ID de la API
    service_id = Column(Integer, ForeignKey("services.id"))
    escalation_policy_id = Column(Integer, ForeignKey('escalation_policies.id'), nullable=True)  # Relación con política de escalamiento
    status = Column(String(50), nullable=False)
    urgency = Column(String(50), nullable=False)
    summary = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    service = relationship("Service", back_populates="incidents")
    escalation_policy = relationship("EscalationPolicy", back_populates="incidents")
    teams = relationship("IncidentTeam", back_populates="incident")