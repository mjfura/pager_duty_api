from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.config import Base

class EscalationPolicy(Base):
    __tablename__ = "escalation_policies"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe

    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(String(50), unique=True, nullable=False)  # ID de la API
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    services = relationship("ServiceEscalationPolicy", back_populates="escalation_policy")
    teams = relationship("TeamEscalationPolicy", back_populates="escalation_policy")
    incidents = relationship("Incident", back_populates="escalation_policy")