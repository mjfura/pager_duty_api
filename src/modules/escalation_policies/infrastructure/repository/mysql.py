from src.modules.escalation_policies.domain import EscalationPoliciesRepository
from ..models import EscalationPolicy
from src.modules.teams.infrastructure.models import Team,TeamEscalationPolicy
from src.modules.services.infrastructure.models import Service,ServiceEscalationPolicy
from typing import List
class MySQLEscalationPoliciesRepository(EscalationPoliciesRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def insert_escalation_policies(self, escalation_policies: List[dict]) -> List[str]:
        ids=[]
        for policy in escalation_policies:
            db_escalation_policy = EscalationPolicy(
                policy_id=policy['id'],
                name=policy.get('name'),
                description=policy.get('description')
            )
            self.db_session.merge(db_escalation_policy)
            self.db_session.commit()
            id_local = db_escalation_policy.id
            for team in policy.get('teams', []):
                team_data = self.db_session.query(Team).filter_by(team_id=team['id']).first()
                if not team_data:
                    continue
                db_team_escalation_policy = TeamEscalationPolicy(
                    escalation_policy_id=id_local,
                    team_id=team_data.id
                )
                self.db_session.merge(db_team_escalation_policy)
                self.db_session.commit()
            for service in policy.get('services', []):
                service_data = self.db_session.query(Service).filter_by(service_id=service['id']).first()
                if not service_data:
                    continue
                db_service_escalation_policy = ServiceEscalationPolicy(
                    escalation_policy_id=id_local,
                    service_id=service_data.id
                )
                self.db_session.merge(db_service_escalation_policy)
                self.db_session.commit()
            ids.append(id_local)
        return ids
    
    def get_escalation_policies_services_teams(self)->List[dict]:
        policies = self.db_session.query(EscalationPolicy).all()
        result = []
        for policy in policies:
            services = self.db_session.query(ServiceEscalationPolicy).filter_by(escalation_policy_id=policy.id).all()
            teams = self.db_session.query(TeamEscalationPolicy).filter_by(escalation_policy_id=policy.id).all()
            result.append({
                'escalation_policy_id':policy.policy_id,
                'escalation_policy_name':policy.name,
                'escalation_policy_description':policy.description,
                'services':len(services),
                'teams':len(teams)
            })
        return result