from flask import Blueprint
from src.modules.services.infrastructure.controllers.service import ServicesController
from src.modules.services.application import ServicesUseCase
from src.modules.services.infrastructure.repository import MySQLServicesRepository
from src.config import db_session
import pandas as pd
from flask import Response
services_bp = Blueprint('services', __name__)


@services_bp.route('/quantity', methods=['GET'])
def count_services():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    return{
        'total':services_controller.count_services()
    }

@services_bp.route('/export_csv', methods=['GET'])
def export_csv():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    services=services_controller.get_services()
    services_pd = pd.DataFrame(services)
    response = Response(services_pd.to_csv(index=False), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=report_services.csv"
    return response

@services_bp.route('/incidents_export_csv', methods=['GET'])
def incidents_export_csv():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    incidents=services_controller.get_incidents_by_services()
    incidents_pd = pd.DataFrame(incidents)
    response = Response(incidents_pd.to_csv(index=False), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=report_services_incidents.csv"
    return response

@services_bp.route('/incidents', methods=['GET'])
def get_services_incidents():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    return{
        'services':services_controller.get_incidents_by_services()
    }

@services_bp.route('/incidents_status_export_csv', methods=['GET'])
def incidents_status_export_csv():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    incidents=services_controller.get_incidents_by_services_and_status()
    incidents_pd = pd.DataFrame(incidents)
    response = Response(incidents_pd.to_csv(index=False), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=report_services_incidents_status.csv"
    return response


@services_bp.route('/incidents_status', methods=['GET'])
def get_services_incidents_status():
    service_repository = MySQLServicesRepository(db_session)
    services_use_case = ServicesUseCase(service_repository)
    services_controller = ServicesController(services_use_case)
    return{
        'services':services_controller.get_incidents_by_services_and_status()
   }