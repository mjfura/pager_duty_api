from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config import Base

class ServiceTeam(Base):
    __tablename__ = "service_teams"
    __table_args__ = {'extend_existing': True}  # Permite redefinir si ya existe
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    # Relaciones
    service = relationship("Service", back_populates="teams")
    team = relationship("Team", back_populates="services")