from ..domain import IncidentsRepository
from typing import List
class IncidentsUseCase:
    def __init__(self, incidents_repository:IncidentsRepository):
        self.incidents_repository = incidents_repository

    def insert_incidents(self, incidents: List[dict]) -> List[str]:
        return self.incidents_repository.insert_incidents(incidents)
    
    def get_incidents_breakdown(self)->dict:
        return self.incidents_repository.get_incidents_breakdown()