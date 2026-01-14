from core.models import ApplicationCreate, TaskCreate
from repository.application_repository import ApplicationRepository

class ApplicationService:
    def __init__(self, repository: ApplicationRepository = None):
        self.repository = repository or ApplicationRepository()

    async def list_applications(self):
        """Fetch all scholarship applications from the database."""
        try:
            return await self.repository.get_all()
        except Exception as e:
            print(f"❌ Error listing applications: {e}")
            return {"error": str(e)}

    async def get_application_by_id(self, application_id: str):
        """Fetch a scholarship application by its ID."""
        try:
            return await self.repository.get_by_id(application_id)
        except Exception as e:
            print(f"❌ Error fetching application by ID: {e}")
            return {"error": str(e)}

    async def create_application(self, application_data: ApplicationCreate):
        """Membuat aplikasi beasiswa baru"""
        try:
            return await self.repository.create(application_data)
        except Exception as e:
            print(f"❌ Error creating application: {e}")
            return {"error": str(e)}

    async def create_task(self, task_data: TaskCreate):
        """Membuat task baru untuk aplikasi"""
        try:
            return await self.repository.create_task(task_data)
        except Exception as e:
            print(f"❌ Error creating task: {e}")
            return {"error": str(e)}

    async def get_tasks_by_application_id(self, application_id: str):
        """Fetch all tasks associated with a specific application ID."""
        try:
            return await self.repository.get_tasks_by_app_id(application_id)
        except Exception as e:
            print(f"❌ Error fetching tasks by application ID: {e}")
            return {"error": str(e)}
