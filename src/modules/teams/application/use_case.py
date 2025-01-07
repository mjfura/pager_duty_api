from ..domain import TeamsRepository
from typing import List
class TeamsUseCase:
    def __init__(self, teams_repository:TeamsRepository):
        self.teams_repository = teams_repository

    def insert_teams(self, teams: List[dict]) -> List[str]:
        return self.teams_repository.insert_teams(teams)
    
    def get_teams_services(self)->List[dict]:
        return self.teams_repository.get_teams_services()