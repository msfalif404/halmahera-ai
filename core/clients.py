from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings
from config.settings import (
    HOST_ELASTICSEARCH, API_KEY_ELASTICSEARCH, OPENAI_API_KEY
)

class ElasticsearchClient:
    def __init__(self):
        self.client = None
        self._initialize()
    
    def _initialize(self):
        try:
            self.client = Elasticsearch([HOST_ELASTICSEARCH], api_key=API_KEY_ELASTICSEARCH)
            if not self.client.ping():
                raise ConnectionError("Koneksi ke Elasticsearch gagal.")
            print("✅ Terhubung ke Elasticsearch!")
        except Exception as e:
            print(f"❌ Error koneksi ke Elasticsearch: {e}")
            # exit() # Better not to crash imports if connection fails during dev
    
    def get_client(self):
        return self.client

class EmbeddingClient:
    def __init__(self):
        self.embedding = None
        self._initialize()
    
    def _initialize(self):
        try:
            self.embedding = OpenAIEmbeddings(
                openai_api_key=OPENAI_API_KEY
            )
            print(f"✅ OpenAI Embeddings siap digunakan.")
        except Exception as e:
            print(f"❌ Error inisialisasi OpenAIEmbeddings: {e}")
            # exit()
    
    def get_embedding(self):
        return self.embedding

# Singleton instances
es_client = ElasticsearchClient().get_client()
embedding_client = EmbeddingClient().get_embedding()