from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base

class IncidentTeam(Base):
    __tablename__ = "incident_teams"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    # Relaciones
    incident = relationship("Incident", back_populates="teams")
    team = relationship("Team", back_populates="incidents")