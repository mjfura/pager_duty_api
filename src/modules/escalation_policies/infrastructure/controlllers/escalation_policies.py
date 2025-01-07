from src.modules.escalation_policies.application import EscalationPoliciesUseCase
from typing import List
class EscalationPoliciesController:
    def __init__(self, escalation_policies_use_case: EscalationPoliciesUseCase):
        self.escalation_policies_use_case = escalation_policies_use_case
    
    def get_escalation_policies_services_teams(self)->List[dict]:
        return self.escalation_policies_use_case.get_escalation_policies_services_teams()