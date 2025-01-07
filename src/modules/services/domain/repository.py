from abc import ABC, abstractmethod
from typing import List
class ServicesRepository(ABC):
    @abstractmethod
    def insert_services(self, services: List[dict]) -> List[str]:
        pass
    
    @abstractmethod
    def get_services(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_quantity_services(self) -> int:
        pass
    
    @abstractmethod
    def get_incidents_by_services(self)->List[dict]:
        pass
    
    @abstractmethod
    def get_incidents_by_services_and_status(self)->List[dict]:
        pass