from repository.scholarship_repository import ScholarshipRepository

class ScholarshipService:
    def __init__(self, repository: ScholarshipRepository = None):
        self.repository = repository or ScholarshipRepository()
    
    def get_all_scholarships(self, limit: int = 100):
        """Ambil semua dokumen beasiswa dari Elasticsearch."""
        try:
            return self.repository.get_all(limit)
        except Exception as e:
            print(f"❌ Error saat mengambil semua beasiswa: {e}")
            return {"error": str(e)}
    
    def search_scholarships(self, query: str, k: int = 5):
        """Pencarian beasiswa berbasis KNN dan text matching."""
        try:
            results = self.repository.search(query, k)
            return {"query": query, "results": results}
        except Exception as e:
            print(f"❌ Error saat search: {e}")
            return {"error": str(e)}