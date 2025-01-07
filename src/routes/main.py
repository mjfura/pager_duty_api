
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
    # for team in teams.json()['teams']:
    #     db_team = Team(
    #         team_id=team['id'],
    #         name=team.get('name'),
    #         description=team.get('description')
    #     )
    #     db_session.merge(db_team)
    #     db_session.commit()
    #     id_local = db_team.id
    #     print(f'ID LOCAL {id_local}')
    response = client.get('/services',params={
    "limit": 100
    })
    services_ids = [service['id'] for service in response.json()['services']]
    services_use_case.insert_services(response.json()['services'])
    # for service in response.json()['services']:
    #     db_service = Service(
    #         service_id=service['id'],
    #         name=service.get('name'),
    #         description=service.get('description'),
    #         status=service.get('status'),
    #         created_at=isoparse(service['created_at']),
    #         updated_at=isoparse(service['updated_at'])
    #     )
    #     db_session.merge(db_service)
    #     db_session.commit()
    #     id_local = db_service.id
    #     print(f'ID LOCAL {id_local}')
    #     teams_service = service.get('teams', [])
    #     for team in teams_service:
    #         team_data = db_session.query(Team).filter_by(team_id=team['id']).first()
    #         if not team_data:
    #             continue
    #         db_service_team = ServiceTeam(
    #             service_id=id_local,
    #             team_id=team_data.id
    #         )
    #         db_session.merge(db_service_team)
    #         db_session.commit()
    #     print(f"✅ Servicio {service['name']} guardado correctamente con Teams.")
        
    # print("✅ Servicios guardados correctamente.")

    
    escalation_policies=client.get('/escalation_policies',params={
    "limit": 100
    }
    )
    escalation_policies_use_case.insert_escalation_policies(escalation_policies.json()['escalation_policies'])
    # for policy in escalation_policies.json()['escalation_policies']:
    #     db_escalation_policy = EscalationPolicy(
    #         policy_id=policy['id'],
    #         name=policy.get('name'),
    #         description=policy.get('description')
    #     )
    #     db_session.merge(db_escalation_policy)
    #     db_session.commit()
    #     id_local = db_escalation_policy.id
    #     for team in policy.get('teams', []):
    #         team_data = db_session.query(Team).filter_by(team_id=team['id']).first()
    #         if not team_data:
    #             continue
    #         db_team_escalation_policy = TeamEscalationPolicy(
    #             escalation_policy_id=id_local,
    #             team_id=team_data.id
    #         )
    #         db_session.merge(db_team_escalation_policy)
    #         db_session.commit()
    #     for service in policy.get('services', []):
    #         service_data = db_session.query(Service).filter_by(service_id=service['id']).first()
    #         if not service_data:
    #             continue
    #         db_service_escalation_policy = ServiceEscalationPolicy(
    #             escalation_policy_id=id_local,
    #             service_id=service_data.id
    #         )
    #         db_session.merge(db_service_escalation_policy)
    #         db_session.commit()
    #     print(f'ID LOCAL {id_local}')
    
    
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
        # for incident in incidents:
        #     db_incident = Incident(
        #         incident_id=incident['id'],
        #         service_id=db_session.query(Service).filter_by(service_id=incident['service']['id']).first().id,
        #         escalation_policy_id = db_session.query(EscalationPolicy).filter_by(policy_id=incident['escalation_policy']['id']).first().id,
        #         status=incident.get('status'),
        #         urgency=incident.get('urgency'),
        #         summary=incident.get('summary'),
        #         created_at=isoparse(incident['created_at']),
        #         updated_at=isoparse(incident['updated_at'])
        #     )
        #     db_session.merge(db_incident)
        #     db_session.commit()
        #     id_local = db_incident.id
        #     teams_incident = incident.get('teams', [])
        #     for team in teams_incident:
        #         team_data = db_session.query(Team).filter_by(team_id=team['id']).first()
        #         if not team_data:
        #             continue
        #         db_incident_team = IncidentTeam(
        #             incident_id=id_local,
        #             team_id=team_data.id
        #         )
        #         db_session.merge(db_incident_team)
        #         db_session.commit()
        #     print(f'ID LOCAL {id_local}')
            
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