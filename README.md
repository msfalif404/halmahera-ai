# AI Agent Scholarship Application

A FastAPI-based scholarship search and application management system powered by OpenAI, Elasticsearch, and **LangGraph**.

## 🚀 Features

- **🤖 AI Agent**: Integrated LangGraph agent (`POST /chat`) that orchestrates the entire application process via natural language.
- **Semantic Search**: AI-powered scholarship search using OpenAI embeddings.
- **Service-Repository Pattern**: Clean architecture separating business logic from data access.
- **Application Management**: Track and manage scholarship applications.
- **Task Planning**: Create personalized preparation roadmaps.
- **Elasticsearch Integration**: Fast and scalable search capabilities.
- **PostgreSQL Database**: Reliable data persistence.
- **Docker Support**: Containerized deployment.

## 🏗️ Project Structure

```
.
├── agent/                        # AI Agent Layer (LangGraph)
│   ├── graph.py                  # State Graph Definition
│   └── routes.py                 # Chat Endpoint
├── api/                          # API layer
├── config/                       # Configuration management
├── controller/                   # Business logic controllers
├── core/                         # Core infrastructure
├── repository/                   # Data Access Layer
├── scripts/                      # Utility scripts
├── service/                      # Service layer
├── docker-compose.yml            # Elasticsearch container
├── Dockerfile                    # Multi-stage Python build
├── main.py                       # FastAPI application entry point
└── requirements.txt              # Python dependencies
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12
- **Agent Orchestration**: LangGraph, LangChain
- **AI/ML**: OpenAI (Embeddings & Chat)
- **Search**: Elasticsearch 7.17
- **Database**: PostgreSQL (Neon)
- **Deployment**: Docker

## 🔗 API Endpoints

### 🤖 AI Agent
- `POST /chat` - Interact with the Scholarship Assistant Agent.
  - Body: `{"message": "I want to apply for..."}`

### Scholarships
- `GET /` - List all scholarships (limit: 100)
- `GET /search?query=<text>` - Semantic search for scholarships

### Applications
- `POST /applications` - Create new application
- `GET /applications` - List user applications

### Tasks
- `POST /tasks` - Create preparation tasks

## ⚙️ Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** in `.env`:
   ```env
   HOST_ELASTICSEARCH=<host>
   API_KEY_ELASTICSEARCH=<key>
   OPENAI_API_KEY=<key>
   ```
4. **Start Infrastructure**
   ```bash
   docker-compose up -d
   ```
5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 📊 Architecture

The application combines a standard **Service-Repository** architecture with an **Agentic Layer**:

1.  **Agent Layer** (`agent/`): The "Brain". Uses LangGraph to decide which tools to call based on user intent.
2.  **Controller Layer** (`controller/`): The "Tools". Exposes business capabilities to both the API and the Agent.
3.  **Service/Repository**: Handles logic and data persistence.
