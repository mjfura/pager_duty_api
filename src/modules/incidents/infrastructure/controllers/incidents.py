from src.modules.incidents.application import IncidentsUseCase

class IncidentsController:
    def __init__(self, incidents_use_case: IncidentsUseCase):
        self.incidents_use_case = incidents_use_case

    def export_csv_incidents_breakdown(self)->dict:
        return self.incidents_use_case.get_incidents_breakdown()