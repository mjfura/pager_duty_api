from src.modules.services.domain import ServicesRepository
from typing import List
from ..models import Service,ServiceTeam
from src.modules.teams.infrastructure.models import Team
from src.modules.incidents.infrastructure.models import Incident
from dateutil.parser import isoparse

class MySQLServicesRepository(ServicesRepository):
    def __init__(self,db_session):
        self.db_session = db_session
        
    def insert_services(self, services: List[dict]) -> List[str]:
        ids=[]
        for service in services:
            db_service = Service(
                service_id=service['id'],
                name=service.get('name'),
                description=service.get('description'),
                status=service.get('status'),
                created_at=isoparse(service['created_at']),
                updated_at=isoparse(service['updated_at'])
            )
            self.db_session.merge(db_service)
            self.db_session.commit()
            id_local = db_service.id
            ids.append(id_local)
            teams_service = service.get('teams', [])
            for team in teams_service:
                team_data = self.db_session.query(Team).filter_by(team_id=team['id']).first()
                if not team_data:
                    continue
                db_service_team = ServiceTeam(
                    service_id=id_local,
                    team_id=team_data.id
                )
                self.db_session.merge(db_service_team)
                self.db_session.commit()
        return ids
    
    def get_quantity_services(self)->int:
        return self.db_session.query(Service).count()
    
    def get_incidents_by_services(self)->List[dict]:
        services = self.db_session.query(Service).all()
        result = []
        for service in services:
            incidents = self.db_session.query(Incident).filter_by(service_id=service.id).all()
            result.append({
                'service_id':service.service_id,
                'service':service.name,
                'service_description':service.description,
                'service_status':service.status,
                'quantity_incidents':len(incidents)
            })
        return result
    def get_incidents_by_services_and_status(self)->List[dict]:
        services = self.db_session.query(Service).all()
        result = []
        for service in services:
            incidents = self.db_session.query(Incident).filter_by(service_id=service.id).all()
            result.append({
                'service_id':service.service_id,
                'service':service.name,
                'service_description':service.description,
                'service_status':service.status,
                'incidents_triggered':len([incident for incident in incidents if incident.status == 'triggered']),
                'incidents_acknowledged':len([incident for incident in incidents if incident.status == 'acknowledged']),
                'incidents_resolved':len([incident for incident in incidents if incident.status == 'resolved'])
            })
        return result
    
    def get_services(self):
        services = self.db_session.query(Service).all()
        result=[]
        for service in services:
            result.append({
                'id':service.service_id,
                'name':service.name,
                'description':service.description,
                'status':service.status,
                'created_at':service.created_at,
                'updated_at':service.updated_at
            })
        return result