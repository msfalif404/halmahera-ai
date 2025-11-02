from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from langchain_ibm import WatsonxEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# =========================
# KONFIGURASI DASAR
# =========================
ES_INDEX = "scholarship_vector_index"
HOST_ELASTICSEARCH = "http://localhost:9200"

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_URL = os.getenv('WATSONX_URL')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
WATSONX_MODEL_ID = os.getenv('WATSONX_MODEL_ID')

# =========================
# INISIALISASI CLIENT
# =========================
try:
    es_client = Elasticsearch([HOST_ELASTICSEARCH])
    if not es_client.ping():
        raise ConnectionError("Koneksi ke Elasticsearch gagal.")
    print("✅ Terhubung ke Elasticsearch!")
except Exception as e:
    print(f"❌ Error koneksi ke Elasticsearch: {e}")
    exit()

embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 512,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}

try:
    watsonx_embedding = WatsonxEmbeddings(
        apikey=WATSONX_API_KEY,
        model_id=WATSONX_MODEL_ID,
        url=WATSONX_URL,
        project_id=WATSONX_PROJECT_ID,
        params=embed_params,
    )
    print(f"✅ Watsonx model '{WATSONX_MODEL_ID}' siap digunakan.")
except Exception as e:
    print(f"❌ Error inisialisasi WatsonxEmbeddings: {e}")
    exit()

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Scholarship Search API (All Fields)")

# 🟢 Root endpoint menampilkan semua data
@app.get("/")
def get_all_scholarships(limit: int = 100):
    """
    Ambil semua dokumen beasiswa dari Elasticsearch.
    """
    try:
        search_body = {
            "size": limit,
            "query": {"match_all": {}},
            "_source": {
                "excludes": ["embedding", "score", "image"]
            }
        }
        results = es_client.search(index=ES_INDEX, body=search_body)

        all_scholarships = [
            hit["_source"]
            for hit in results["hits"]["hits"]
        ]

        return {"count": len(all_scholarships), "results": all_scholarships}

    except Exception as e:
        print(f"❌ Error saat mengambil semua beasiswa: {e}")
        return {"error": str(e)}

# 🔍 Endpoint search tetap sama
@app.get("/search")
def search_scholarship(query: str = Query(..., description="Teks pencarian"), k: int = 5):
    """
    Endpoint untuk melakukan pencarian berbasis KNN di Elasticsearch.
    Mengembalikan seluruh field dari dokumen (kecuali embedding).
    """
    try:
        # 1️⃣ Buat embedding dari query
        query_vector = watsonx_embedding.embed_query(query.lower())

        # 2️⃣ Susun query body
        search_body = {
            "size": k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "_source": {
                "excludes": ["embedding", "score", "image"]
            }
        }

        # 3️⃣ Eksekusi pencarian
        results = es_client.search(index=ES_INDEX, body=search_body)

        # 4️⃣ Format hasil
        formatted_results = [
            hit["_source"]
            for hit in results["hits"]["hits"]
        ]

        return {"query": query, "results": formatted_results}

    except Exception as e:
        print(f"❌ Error saat search: {e}")
        return {"error": str(e)}
