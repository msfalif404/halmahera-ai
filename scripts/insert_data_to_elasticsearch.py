import json
import os
import sys

# Add parent directory to path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from elasticsearch import helpers
from core.clients import es_client, embedding_client
from config.settings import ES_INDEX

EMBEDDING_DIM = 1536 # OpenAI text-embedding-3-small dimension (or 1536 for ada-002)

def delete_index_if_exists(index_name):
    try:
        es_client.indices.delete(index='*', ignore=[400, 404])
        # es_client.indices.delete(index=index_name, ignore=[404])
        print("✅ Semua indices berhasil dihapus!")
    except Exception as e:
        print(f"Error menghapus indeks: {e}")

def load_data_from_json(filepath="scholarships.json"):
    # Adjust filepath since we are in scripts/
    filepath = os.path.join(os.path.dirname(__file__), filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Berhasil memuat {len(data)} dokumen dari {filepath}.")
        return data
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' bukan JSON yang valid.")
        return []


def create_vector_index():
    if es_client.indices.exists(index=ES_INDEX):
        print(f"Indeks '{ES_INDEX}' sudah ada. Melewati pembuatan mapping.")
        return

    mapping = {
        "mappings": {
            "properties": {
                "embedding": {
                    "type": "dense_vector",
                    "dims": EMBEDDING_DIM  
                },
                
                "id": {"type": "text"},
                "name": {"type": "text"},
                "description": {"type": "text"},
                "deadline": {"type": "date"},
                
                "location": {"type": "text"},
                "university": {"type": "text"},
                "image": {"type": "text"},
                "degree": {"type": "text"},
                "fields": {"type": "text"},
                "tags": {"type": "text"},
                "url": {"type": "text"},
                "need_ielts": {"type": "boolean"},
                "need_scholastic": {"type": "boolean"},
                "need_essay": {"type": "boolean"},
            }
        }
    }
    es_client.indices.create(index=ES_INDEX, ignore=400, body=mapping)
    print(f"Indeks '{ES_INDEX}' berhasil dibuat dengan mapping yang sesuai.")

def generate_and_index_data(documents):
    actions = []

    def to_bool(value):
        """Konversi aman ke boolean untuk field seperti need_ielts, need_essay, dll"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ["true", "yes", "y", "1"]
        if isinstance(value, int):
            return value == 1
        return False

    for idx, doc in enumerate(documents, 1):
        try:
            text_to_embed = f"{doc.get('name', '')}. {doc.get('description', '')}"
            print(f"({idx}/{len(documents)}) Membuat embedding untuk: {doc.get('name', 'Unknown')}")
            vector = embedding_client.embed_query(text_to_embed)

            # OpenAI returns a flat list (already normalized usually)
            final_vector = vector
            
            document_to_index = {
                "_index": ES_INDEX,
                "_source": {
                    "id": doc.get("id", ""),
                    "name": doc.get("name", ""),
                    "description": doc.get("description", ""),
                    "deadline": doc.get("deadline", None),  
                    "location": doc.get("location", ""),
                    "university": doc.get("university", ""),
                    "image": doc.get("image", ""),
                    "degree": doc.get("degree", ""),
                    "fields": doc.get("fields", ""),
                    "tags": doc.get("tags", []),
                    "url": doc.get("url", ""),

                    "need_ielts": to_bool(doc.get("need_ielts", False)),
                    "need_scholastic": to_bool(doc.get("need_scholastic", False)),
                    "need_essay": to_bool(doc.get("need_essay", False)),

                    "embedding": final_vector
                }
            }

            actions.append(document_to_index)

        except Exception as e:
            print(f"⚠️ Gagal memproses dokumen '{doc.get('name', 'Unknown')}': {e}")
            continue

    print(f"\nMemulai indexing untuk {len(actions)} dokumen...")
    success, errors = helpers.bulk(es_client, actions, raise_on_error=False)
    print(f"Indeks selesai. Berhasil mengindeks {success} dokumen. Total error: {len(errors)}")

def perform_knn_search(query_text, k=5):
    print(f"\n🔍 Mencari: '{query_text}'...")

    query_vector = embedding_client.embed_query(query_text.lower())

    search_fields = [
        "name^5",          
        "description^4",
        "university^3",
        "degree^2",
        "fields^2",
        "location^1",
        "tags^1"
    ]

    search_body = {
        "size": k,
        "query": {
            "script_score": {
                "query": {
                    "multi_match": {
                        "query": query_text,
                        "fields": search_fields,
                        "type": "best_fields",
                        "operator": "or",
                        "fuzziness": "AUTO"
                    }
                },
                "script": {
                    "source": """
                        double textScore = _score;
                        double vectorScore = cosineSimilarity(params.query_vector, 'embedding');
                        return 0.7 * vectorScore + 0.3 * textScore;
                    """,
                    "params": {"query_vector": query_vector}
                }
            }
        },
        "_source": [
            "id", "name", "description", "deadline", "location", 
            "university", "degree", "fields", "tags", "url"
        ]
    }

    try:
        results = es_client.search(index=ES_INDEX, body=search_body)
        hits = results["hits"]["hits"]

        print(f"\n*** Hasil Pencarian untuk: '{query_text}' ***")
        print(f"Ditemukan {len(hits)} hasil\n")

        for i, hit in enumerate(hits, 1):
            src = hit["_source"]
            print(f"{i}. Skor gabungan: {hit['_score']:.4f}")
            print(f"   🎓 {src.get('name', '-')}")
            print(f"   🏛️ Universitas: {src.get('university', '-')}")
            print(f"   📝 Deskripsi: {src.get('description', '')[:100]}...\n")

        return results

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    scholarship_data = load_data_from_json("scholarships.json")
    regenerate_index = True

    if regenerate_index:
        delete_index_if_exists(ES_INDEX)
        create_vector_index()
        generate_and_index_data(scholarship_data)

    if scholarship_data:
        perform_knn_search("I want to apply for a scholarship in the field of Artificial Intelligence.")