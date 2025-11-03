from fastapi import APIRouter, Query

from controller.application_controller import ApplicationController
from controller.scholarship_controller import ScholarshipController
from core.models import ApplicationCreate, TaskCreate

router = APIRouter()


@router.get("/")
def get_all_scholarships(limit: int = 100):
    """Get all scholarships with an optional limit."""
    return ScholarshipController.get_all_scholarships(limit)


@router.get("/search")
def search_scholarship(query: str = Query(..., description="Teks pencarian")):
    """
    Perform a search for scholarships based on a query string.

    Args:
        query (str): The search query string.

    Returns:
        A list of scholarships matching the search criteria.
    """
    return ScholarshipController.search_scholarship(query, k=10)


@router.post("/applications")
async def create_application(application_data: ApplicationCreate):
    """
    Create a new scholarship application for user to prepare the scholarship application.

    Args:
        application_data (ApplicationCreate): The data for the new application.

    Returns:
        The created application object.
    """
    return await ApplicationController.create_application(application_data)


@router.get("/applications")
async def list_applications():
    """List all scholarship applications."""

    return await ApplicationController.list_applications()


@router.get("/applications/{application_id}")
async def get_application_by_id(application_id: str):
    """Get a scholarship application by its ID."""
    return await ApplicationController.get_application_by_id(application_id)


@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    """Membuat task baru untuk aplikasi."""
    return await ApplicationController.create_task(task_data)


@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str):
    """Get a task by its ID."""
    return await ApplicationController.get_task_by_id(task_id)
