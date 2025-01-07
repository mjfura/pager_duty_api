from typing import List
from src.modules.teams.domain import TeamsRepository
from src.modules.services.infrastructure.models import ServiceTeam
from ..models import Team

class MySQLTeamsRepository(TeamsRepository):
    def __init__(self,db_session):
        self.db_session = db_session
        
    def insert_teams(self, teams: List[dict]) -> List[str]:
        ids=[]
        for team in teams:
            db_team = Team(
                team_id=team['id'],
                name=team.get('name'),
                description=team.get('description')
            )
            self.db_session.merge(db_team)
            self.db_session.commit()
            ids.append(db_team.id)
        return ids
    
    def get_teams_services(self)->List[dict]:
        teams = self.db_session.query(Team).all()
        result = []
        for team in teams:
            services = self.db_session.query(ServiceTeam).filter_by(team_id=team.id).all()
            result.append({
                'team':team.name,
                'team_id':team.team_id,
                'team_description':team.description,
                'quantity_services':len(services)
            })
        return result