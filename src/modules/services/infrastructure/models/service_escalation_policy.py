from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base

class ServiceEscalationPolicy(Base):
    __tablename__ = "service_escalation_policies"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    escalation_policy_id = Column(Integer, ForeignKey("escalation_policies.id"))
    
    # Relaciones
    service = relationship("Service", back_populates="escalation_policies")
    escalation_policy = relationship("EscalationPolicy", back_populates="services")