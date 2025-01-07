
from ..config import app,client,db_session
from src.modules.teams.infrastructure.repository import MySQLTeamsRepository
from src.modules.teams.application import TeamsUseCase
from src.modules.services.infrastructure.repository import MySQLServicesRepository
from src.modules.services.application import ServicesUseCase
from src.modules.escalation_policies.infrastructure.repository import MySQLEscalationPoliciesRepository
from src.modules.escalation_policies.application import EscalationPoliciesUseCase
from src.modules.incidents.infrastructure.repository import MySQLIncidentsRepository
from src.modules.incidents.application import IncidentsUseCase
from src.modules.services.infrastructure.routes import services_bp
from src.modules.teams.infrastructure.routes import teams_bp
from src.modules.escalation_policies.infrastructure.routes import escalation_policies_bp
from src.modules.incidents.infrastructure.routes import incidents_bp
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(teams_bp, url_prefix='/teams')
app.register_blueprint(escalation_policies_bp, url_prefix='/escalation_policies')
app.register_blueprint(incidents_bp, url_prefix='/incidents')

@app.route('/export_csv', methods=['GET'])
def export_csv():
    teams_repository = MySQLTeamsRepository(db_session)
    teams_use_case = TeamsUseCase(teams_repository)
    services_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(services_repository)
    escalation_policies_repository = MySQLEscalationPoliciesRepository(db_session)
    escalation_policies_use_case = EscalationPoliciesUseCase(escalation_policies_repository)
    incidents_repository = MySQLIncidentsRepository(db_session)
    incidents_use_case = IncidentsUseCase(incidents_repository)
    teams_use_case.export_csv()
    services_use_case.export_csv()
    escalation_policies_use_case.export_csv()
    incidents_use_case.export_csv()
    return {
        'message':'CSV Exported'
    }

@app.route('/load_data', methods=['GET'])
def load_data():
    teams = client.get('/teams')
    teams_repository = MySQLTeamsRepository(db_session)
    teams_use_case = TeamsUseCase(teams_repository)
    services_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(services_repository)
    escalation_policies_repository = MySQLEscalationPoliciesRepository(db_session)
    escalation_policies_use_case = EscalationPoliciesUseCase(escalation_policies_repository)
    incidents_repository = MySQLIncidentsRepository(db_session)
    incidents_use_case = IncidentsUseCase(incidents_repository)
    
    teams_use_case.insert_teams(teams.json()['teams'])
 
    response = client.get('/services',params={
    "limit": 100
    })
    services_ids = [service['id'] for service in response.json()['services']]
    services_use_case.insert_services(response.json()['services'])
    
    
    escalation_policies=client.get('/escalation_policies',params={
    "limit": 100
    }
    )
    escalation_policies_use_case.insert_escalation_policies(escalation_policies.json()['escalation_policies'])
    
    
    offset = 0
    limit = 100
    all_incidents = []
    while True:
        response_incidents = client.get('/incidents', params={
            "service_ids[]": services_ids,
            "since": "2024-01-01T00:00:00Z",
            "limit": limit,
            "offset": offset,
        })
        
        if response_incidents.status_code != 200:
            raise Exception(f"Error: {response_incidents.status_code} - {response_incidents.json()}")

        data = response_incidents.json()
        incidents = data.get('incidents', [])
        incidents_use_case.insert_incidents(incidents)
       
        all_incidents.extend(incidents)

        if not data.get('more', False):
            break

        offset += limit

    
    
    result = {
        'message':'Hola mundo desde Flask',
        'services':response.json(),
        'services_number':len(response.json()['services']),
        'incidents':all_incidents,
        'incidents_number':len(all_incidents),
        'teams':teams.json(),
        'teams_number':len(teams.json()['teams']),
        'escalation_policies':escalation_policies.json(),
        'escalation_policies_number':len(escalation_policies.json()['escalation_policies']),
    }

    return result