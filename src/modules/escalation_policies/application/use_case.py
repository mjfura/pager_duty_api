from ..domain import EscalationPoliciesRepository
from typing import List
class EscalationPoliciesUseCase:
    def __init__(self, escalation_policies_repository:EscalationPoliciesRepository):
        self.escalation_policies_repository = escalation_policies_repository

    def insert_escalation_policies(self, escalation_policies: List[dict]) -> List[str]:
        return self.escalation_policies_repository.insert_escalation_policies(escalation_policies)
    
    def get_escalation_policies_services_teams(self)->List[dict]:
        return self.escalation_policies_repository.get_escalation_policies_services_teams()