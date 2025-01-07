from src.modules.services.application import ServicesUseCase

class ServicesController:
    def __init__(self, services_use_case: ServicesUseCase):
        self.services_use_case = services_use_case

    def count_services(self):
        return self.services_use_case.count_services()
    
    def get_incidents_by_services(self):
        return self.services_use_case.get_incidents_by_services()
    
    def get_incidents_by_services_and_status(self):
        return self.services_use_case.get_incidents_by_services_and_status()
    
    def get_services(self):
        return self.services_use_case.get_services()