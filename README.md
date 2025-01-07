# Backend API Pager Duty

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory and add the following environment variables:
    ```
    API_KEY_PAGER_DUTY=<API_KEY>
    DB_ROOT_PASSWORD_DEV=<ROOT_PASSWORD>
    DB_DEV=<DB_NAME>
    DB_DEV_USER=<DB_USER>
    DB_DEV_PASSWORD=<DB_PASSWORD>
    ```
3. Run `docker compose -f docker-compose.dev.yaml build`
4. Run `docker compose -f docker-compose.dev.yaml up`
5. Go to `http://localhost:8000/load_data` to load the data from the Pager Duty API to the database.

## API Endpoints

1. `/load_data` - Load data from the Pager Duty API to the database.
2. `/services/quantity` - Get the quantity of services.
3. `/services/export_csv` - Export all services in a CSV file.
4. `/services/incidents` - Get all services with its quantity of incidents.
5. `/services/incidents_export_csv` - Export all services with its quantity of incidents in a CSV file.
6. `/services/incidents_status` - Get all services with its quantity of incidents and its status.
7. `/services/incidents_status_export_csv` - Export all services with its quantity of incidents and its status in a CSV file.
8. `/escalation_policies/services_teams` - Get all escalation policies with its quantity of services and teams.
9. `/escalation_policies/services_teams_export_csv` - Export all escalation policies with its quantity of services and teams in a CSV file.
10. `/teams/services` - Get all teams with its quantity of services.
11. `/teams/services_export_csv` - Export all teams with its quantity of services in a CSV file.