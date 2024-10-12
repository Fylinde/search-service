from fastapi import FastAPI
from app.routes import search_routes

app = FastAPI()

app.include_router(search_routes.router, prefix="/search")
