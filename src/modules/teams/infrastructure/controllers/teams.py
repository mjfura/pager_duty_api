from src.modules.teams.application import TeamsUseCase
from typing import List
class TeamsController:
    def __init__(self, teams_use_case: TeamsUseCase):
        self.teams_use_case = teams_use_case

    def get_teams_services(self) -> List[dict]:
        return self.teams_use_case.get_teams_services()