from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base

class TeamEscalationPolicy(Base):
    __tablename__ = "team_escalation_policies"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    escalation_policy_id = Column(Integer, ForeignKey("escalation_policies.id"))
    
    # Relaciones
    team = relationship("Team", back_populates="escalation_policies")
    escalation_policy = relationship("EscalationPolicy", back_populates="teams")