from fastapi import APIRouter, Query
from controller.scholarship_controller import ScholarshipController
from controller.application_controller import ApplicationController
from core.models import ApplicationCreate, TaskCreate

router = APIRouter()

@router.get("/")
def get_all_scholarships(limit: int = 100):
    """Ambil semua dokumen beasiswa dari Elasticsearch."""
    return ScholarshipController.get_all_scholarships(limit)

@router.get("/search")
def search_scholarship(query: str = Query(..., description="Teks pencarian"), k: int = 5):
    """Endpoint untuk melakukan pencarian berbasis KNN di Elasticsearch."""
    return ScholarshipController.search_scholarship(query, k)

@router.post("/applications")
async def create_application(application_data: ApplicationCreate):
    """Membuat aplikasi beasiswa baru."""
    return await ApplicationController.create_application(application_data)

@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    """Membuat task baru untuk aplikasi."""
    return await ApplicationController.create_task(task_data)