from fastapi import Query
from service.scholarship_service import ScholarshipService

class ScholarshipController:
    
    @staticmethod
    def get_all_scholarships(limit: int = 100):
        """Controller untuk mengambil semua beasiswa."""
        service = ScholarshipService()
        return service.get_all_scholarships(limit)
    
    @staticmethod
    def search_scholarship(query: str = Query(..., description="Teks pencarian"), k: int = 10):
        """Controller untuk pencarian beasiswa."""
        service = ScholarshipService()
        return service.search_scholarships(query, k)