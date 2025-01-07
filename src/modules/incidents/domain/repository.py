from abc import ABC, abstractmethod
from typing import List

class IncidentsRepository(ABC):
    @abstractmethod
    def insert_incidents(self, incidents: List[dict]) -> List[str]:
        pass
    
    @abstractmethod
    def get_incidents_breakdown(self)->dict:
        pass