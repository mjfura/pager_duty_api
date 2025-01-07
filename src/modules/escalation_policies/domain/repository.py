from abc import ABC, abstractmethod
from typing import List

class EscalationPoliciesRepository(ABC):
    @abstractmethod
    def insert_escalation_policies(self, escalation_policies: List[dict]) -> List[str]:
        pass
    
    @abstractmethod
    def get_escalation_policies_services_teams(self)->List[dict]:
        pass