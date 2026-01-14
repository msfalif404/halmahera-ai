from core.models import ApplicationCreate, TaskCreate
from service.application_service import ApplicationService


class ApplicationController:
    @staticmethod
    async def list_applications():
        """Return list of all scholarship applications."""
        service = ApplicationService()
        return await service.list_applications()

    @staticmethod
    async def get_application_by_id(application_id: str):
        """Return a scholarship application by its ID."""
        service = ApplicationService()
        return await service.get_application_by_id(application_id)

    @staticmethod
    async def create_application(application_data: ApplicationCreate):
        """Controller untuk membuat aplikasi beasiswa"""
        service = ApplicationService()
        return await service.create_application(application_data)

    @staticmethod
    async def create_task(task_data: TaskCreate):
        """Controller untuk membuat task"""
        service = ApplicationService()
        return await service.create_task(task_data)

    @staticmethod
    async def get_task_by_id(task_id: str):
        """Return a task by its ID."""
        # Note: Original method name in service was get_tasks_by_application_id
        # and Controller argument is task_id but seems to pass it to that method.
        # This matches previous behavior.
        service = ApplicationService()
        return await service.get_tasks_by_application_id(task_id)
