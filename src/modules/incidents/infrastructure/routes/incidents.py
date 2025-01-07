from flask import Blueprint,jsonify
from src.modules.incidents.infrastructure.controllers import IncidentsController
from src.config import db_session
from src.modules.incidents.infrastructure.repository import MySQLIncidentsRepository
from src.modules.incidents.application import IncidentsUseCase
import io
import base64
import matplotlib.pyplot as plt
incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/breakdown_graph', methods=['GET'])
def incidents_breakdown_export_csv():
     # Crear gráfico
    incidents_repository = MySQLIncidentsRepository(db_session)
    incidents_use_case = IncidentsUseCase(incidents_repository)
    incidents_controller = IncidentsController(incidents_use_case)
    response = incidents_controller.export_csv_incidents_breakdown()
    plt.figure(figsize=(10, 6))
    plt.bar(response['statuses'], response['counts'])
    plt.title('Number of Incidents by Status')
    plt.xlabel('Status')
    plt.ylabel('Number of Incidents')
    plt.tight_layout()
    # Guardar en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    # Devolver imagen en base64
    return jsonify({'graph': f'data:image/png;base64,{img_base64}'})