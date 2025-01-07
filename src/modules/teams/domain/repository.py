from abc import ABC, abstractmethod
from typing import List

class TeamsRepository(ABC):
    @abstractmethod
    def insert_teams(self, teams: List[dict]) -> List[str]:
        pass
    
    @abstractmethod
    def get_teams_services(self) -> List[dict]:
        pass
    