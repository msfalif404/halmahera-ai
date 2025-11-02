import uuid
from datetime import datetime
from core.database import db_client
from core.models import ApplicationCreate, TaskCreate

class ApplicationService:
    
    @staticmethod
    async def create_application(application_data: ApplicationCreate):
        """Membuat aplikasi beasiswa baru"""
        try:
            application_id = str(uuid.uuid4())
            query = """
                INSERT INTO scholarship_applications (id, scholarship_id, user_id, status, created_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
            """
            
            result = await db_client.fetchrow(
                query, 
                application_id,
                application_data.scholarship_id,
                application_data.user_id,
                application_data.status,
                datetime.now()
            )
            
            return dict(result) if result else None
            
        except Exception as e:
            print(f"❌ Error creating application: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def create_task(task_data: TaskCreate):
        """Membuat task baru untuk aplikasi"""
        try:
            task_id = str(uuid.uuid4())
            query = """
                INSERT INTO scholarship_application_tasks (id, name, application_id, description, start_date, end_date, status)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
            """
            
            result = await db_client.fetchrow(
                query,
                task_id,
                task_data.name,
                task_data.application_id,
                task_data.description,
                task_data.start_date,
                task_data.end_date,
                task_data.status
            )
            
            return dict(result) if result else None
            
        except Exception as e:
            print(f"❌ Error creating task: {e}")
            return {"error": str(e)}