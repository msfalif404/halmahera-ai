import uuid
from datetime import datetime
from core.database import db_client
from core.models import ApplicationCreate, TaskCreate

class ApplicationRepository:
    async def get_all(self):
        query = "SELECT * FROM scholarship_applications"
        results = await db_client.fetch(query)
        return [dict(record) for record in results]

    async def get_by_id(self, application_id: str):
        query = "SELECT * FROM scholarship_applications WHERE id = $1"
        result = await db_client.fetchrow(query, application_id)
        return dict(result) if result else None
    
    async def create(self, application_data: ApplicationCreate):
        application_id = str(uuid.uuid4())
        query = """
            INSERT INTO scholarship_applications (id, scholarship_id, user_id, status, created_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """
        # Hardcoded user_id as per original service
        result = await db_client.fetchrow(
            query,
            application_id,
            application_data.scholarship_id,
            "HdaynXVC0R3JGKaBlSJCB4zPu1IvwLRV", 
            application_data.status,
            datetime.now(),
        )
        return dict(result) if result else None

    async def create_task(self, task_data: TaskCreate):
        task_id = str(uuid.uuid4())
        # Convert string (YYYY-MM-DD) to datetime.date
        start_date = datetime.strptime(task_data.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(task_data.end_date, "%Y-%m-%d").date()

        query = """
            INSERT INTO scholarship_application_tasks (
                id, name, application_id, description, is_completed, start_date, due_date
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """
        result = await db_client.fetchrow(
            query,
            task_id,
            task_data.name,
            task_data.application_id,
            task_data.description,
            task_data.is_completed,
            start_date,
            end_date,
        )
        return dict(result) if result else None

    async def get_tasks_by_app_id(self, application_id: str):
        # NOTE: Original query used 'id' instead of 'application_id'. Preserving behavior.
        query = "SELECT * FROM scholarship_application_tasks WHERE id = $1" 
        results = await db_client.fetch(query, application_id)
        return [dict(record) for record in results]
