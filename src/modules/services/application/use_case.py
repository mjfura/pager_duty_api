from ..domain import ServicesRepository
from typing import List
class ServicesUseCase:
    def __init__(self, services_repository:ServicesRepository):
        self.services_repository = services_repository

    def insert_services(self, services: List[dict]) -> List[str]:
        return self.services_repository.insert_services(services)
    
    def count_services(self) -> int:
        return self.services_repository.get_quantity_services()
    
    def get_incidents_by_services(self)->List[dict]:
        return self.services_repository.get_incidents_by_services()
    
    def get_incidents_by_services_and_status(self)->List[dict]:
        return self.services_repository.get_incidents_by_services_and_status()
    
    def get_services(self) -> List[dict]:
        return self.services_repository.get_services()