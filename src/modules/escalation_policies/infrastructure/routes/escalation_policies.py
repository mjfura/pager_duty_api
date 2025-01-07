from flask import Blueprint,Response
from src.modules.escalation_policies.infrastructure.repository import MySQLEscalationPoliciesRepository
from src.modules.escalation_policies.application.use_case import EscalationPoliciesUseCase
from src.modules.escalation_policies.infrastructure.controlllers import EscalationPoliciesController
from src.config import db_session
import pandas as pd
escalation_policies_bp = Blueprint('escalation_policies', __name__)

@escalation_policies_bp.route('/services_teams', methods=['GET'])
def get_services_teams():
    escalation_policies_repository = MySQLEscalationPoliciesRepository(db_session)
    escalation_policies_use_case = EscalationPoliciesUseCase(escalation_policies_repository)
    escalation_policies_controller = EscalationPoliciesController(escalation_policies_use_case)
    return{
        'escalation_policies': escalation_policies_controller.get_escalation_policies_services_teams()
    }

@escalation_policies_bp.route('/services_teams_export_csv', methods=['GET'])
def services_teams_export_csv():
    escalation_policies_repository = MySQLEscalationPoliciesRepository(db_session)
    escalation_policies_use_case = EscalationPoliciesUseCase(escalation_policies_repository)
    escalation_policies_controller = EscalationPoliciesController(escalation_policies_use_case)
    escalation_policies=escalation_policies_controller.get_escalation_policies_services_teams()
    escalation_policies_pd = pd.DataFrame(escalation_policies)
    response = Response(escalation_policies_pd.to_csv(index=False), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=report_escalation_policies_services_teams.csv"
    return response