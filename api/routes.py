from fastapi import APIRouter, Query
from controller.scholarship_controller import ScholarshipController

router = APIRouter()

@router.get("/")
def get_all_scholarships(limit: int = 100):
    """Ambil semua dokumen beasiswa dari Elasticsearch."""
    return ScholarshipController.get_all_scholarships(limit)

@router.get("/search")
def search_scholarship(query: str = Query(..., description="Teks pencarian"), k: int = 5):
    """Endpoint untuk melakukan pencarian berbasis KNN di Elasticsearch."""
    return ScholarshipController.search_scholarship(query, k)