# Halmahera AI - Scholarship Search API

A FastAPI-based scholarship search and application management system powered by OpenAI and Elasticsearch.

## 🏗️ Project Structure

```
Halmahera-AI-IBMCloud/
├── api/                          # API layer
│   ├── __init__.py
│   └── routes.py                 # FastAPI route definitions
├── config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py               # Environment and app settings
├── controller/                   # Business logic controllers
│   ├── __init__.py
│   ├── application_controller.py # Application management
│   └── scholarship_controller.py # Scholarship operations
├── core/                         # Core infrastructure
│   ├── __init__.py
│   ├── clients.py                # External service clients (ES, OpenAI)
│   ├── database.py               # Database connections
│   └── models.py                 # Pydantic data models
├── repository/                   # Data Access Layer
│   ├── __init__.py
│   ├── application_repository.py # DB query encapsulation
│   └── scholarship_repository.py # ES query encapsulation
├── scripts/                      # Utility scripts
│   ├── insert_data_to_elasticsearch.py
│   ├── insert_default_user.py
│   └── scholarships.json         # Sample scholarship data
├── service/                      # Service layer
│   ├── __init__.py
│   ├── application_service.py    # Application business logic
│   └── scholarship_service.py    # Scholarship business logic
├── .dockerignore
├── .env                          # Environment variables
├── .gitignore
├── .python-version
├── docker-compose.yml            # Elasticsearch container
├── Dockerfile                    # Multi-stage Python build
├── main.py                       # FastAPI application entry point
├── Procfile                      # Deployment configuration
├── pyproject.toml                # Project metadata
├── requirements.txt              # Python dependencies
└── uv.lock                       # Dependency lock file
```

## 🚀 Features

- **Semantic Search**: AI-powered scholarship search using OpenAI embeddings
- **Service-Repository Pattern**: Clean architecture separating business logic from data access
- **Application Management**: Track and manage scholarship applications
- **Task Planning**: Create personalized preparation roadmaps
- **Elasticsearch Integration**: Fast and scalable search capabilities
- **PostgreSQL Database**: Reliable data persistence
- **Docker Support**: Containerized deployment

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12
- **AI/ML**: OpenAI (Embeddings), LangChain
- **Search**: Elasticsearch 7.17
- **Database**: PostgreSQL (Neon)
- **Deployment**: Docker, Gunicorn
- **Dependencies**: UV package manager

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- OpenAI API Key
- Elasticsearch instance
- PostgreSQL database

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Halmahera-AI-IBMCloud
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create `.env` file with:
   ```env
   HOST_ELASTICSEARCH=<elasticsearch-host>
   API_KEY_ELASTICSEARCH=<elasticsearch-api-key>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

4. **Start Elasticsearch**
   ```bash
   docker-compose up -d
   ```

5. **Initialize data**
   ```bash
   python scripts/insert_data_to_elasticsearch.py
   python scripts/insert_default_user.py
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 🔗 API Endpoints

### Scholarships
- `GET /` - List all scholarships (limit: 100)
- `GET /search?query=<text>` - Semantic search for scholarships

### Applications
- `POST /applications` - Create new application
- `GET /applications` - List user applications
- `GET /applications/{id}` - Get application details

### Tasks
- `POST /tasks` - Create preparation tasks
- `GET /tasks/{id}` - Get task details

## 🐳 Docker Deployment

```bash
# Build and run
docker build -t halmahera-ai .
docker run -p 8000:8000 halmahera-ai

# Or use with Elasticsearch
docker-compose up --build
```

## 📊 Architecture

The application follows a Service-Repository layered architecture:

1. **API Layer** (`api/`) - HTTP endpoints and request handling.
2. **Controller Layer** (`controller/`) - Orchestrates request flow, interacting with Services.
3. **Service Layer** (`service/`) - Implements business logic and domain rules.
4. **Repository Layer** (`repository/`) - Handles abstract data access (Database/Elasticsearch).
5. **Core Layer** (`core/`) - Shared infrastructure, clients, and data models.
6. **Configuration** (`config/`) - Settings and environment management.