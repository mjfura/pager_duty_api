from flask import Blueprint,Response
from src.modules.teams.infrastructure.controllers.teams import TeamsController
from src.modules.teams.infrastructure.repository.mysql import MySQLTeamsRepository
from src.modules.teams.application import TeamsUseCase
from src.config import db_session
import pandas as pd
teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/services', methods=['GET'])
def get_teams_services():
    teams_repository = MySQLTeamsRepository(db_session)
    teams_use_case = TeamsUseCase(teams_repository)
    teams_controller = TeamsController(teams_use_case)
    return{
        'teams': teams_controller.get_teams_services()
    }

@teams_bp.route('/services_export_csv', methods=['GET'])
def services_export_csv():
    teams_repository = MySQLTeamsRepository(db_session)
    teams_use_case = TeamsUseCase(teams_repository)
    teams_controller = TeamsController(teams_use_case)
    teams_services = teams_controller.get_teams_services()
    teams_services_pd = pd.DataFrame(teams_services)
    response = Response(teams_services_pd.to_csv(index=False), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=report_teams_services.csv"
    return response

