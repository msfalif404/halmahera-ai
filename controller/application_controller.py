from service.application_service import ApplicationService
from core.models import ApplicationCreate, TaskCreate

class ApplicationController:
    
    @staticmethod
    async def create_application(application_data: ApplicationCreate):
        """Controller untuk membuat aplikasi beasiswa"""
        return await ApplicationService.create_application(application_data)
    
    @staticmethod
    async def create_task(task_data: TaskCreate):
        """Controller untuk membuat task"""
        return await ApplicationService.create_task(task_data)