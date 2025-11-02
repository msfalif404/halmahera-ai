from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Scholarship Search API (All Fields)")

app.include_router(router)