from src.modules.incidents.domain import IncidentsRepository
from ..models import Incident,IncidentTeam
from src.modules.services.infrastructure.models import Service
from src.modules.teams.infrastructure.models import Team
from src.modules.escalation_policies.infrastructure.models import EscalationPolicy
from typing import List
from dateutil.parser import isoparse
class MySQLIncidentsRepository(IncidentsRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def insert_incidents(self, incidents: List[dict]) -> List[str]:
        incidents_ids = []
        for incident in incidents:
            db_incident = Incident(
                incident_id=incident['id'],
                service_id=self.db_session.query(Service).filter_by(service_id=incident['service']['id']).first().id,
                escalation_policy_id = self.db_session.query(EscalationPolicy).filter_by(policy_id=incident['escalation_policy']['id']).first().id,
                status=incident.get('status'),
                urgency=incident.get('urgency'),
                summary=incident.get('summary'),
                created_at=isoparse(incident['created_at']),
                updated_at=isoparse(incident['updated_at'])
            )
            self.db_session.merge(db_incident)
            self.db_session.commit()
            id_local = db_incident.id
            teams_incident = incident.get('teams', [])
            for team in teams_incident:
                team_data = self.db_session.query(Team).filter_by(team_id=team['id']).first()
                if not team_data:
                    continue
                db_incident_team = IncidentTeam(
                    incident_id=id_local,
                    team_id=team_data.id
                )
                self.db_session.merge(db_incident_team)
                self.db_session.commit()
            incidents_ids.append(id_local)
        return incidents_ids
    
    def get_incidents_breakdown(self)->dict:
        incidents = self.db_session.query(Incident.status, self.db_session.func.count(Incident.id)).group_by(Incident.status).all()
        
        statuses = [status for status, count in incidents]
        counts = [count for status, count in incidents]
        
        return{
            'statuses':statuses,
            'counts':counts,
            'incidents':incidents
        }