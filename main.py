
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from src.routes import app
from src.config.database import engine, Base
# from src.models import Service,Incident,Team,EscalationPolicy,ServiceTeam,ServiceEscalationPolicy,TeamEscalationPolicy,IncidentTeam


def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    create_tables()
    print("Tablas creadas exitosamente.")
    app.run(debug=True, host='0.0.0.0', port=8000)