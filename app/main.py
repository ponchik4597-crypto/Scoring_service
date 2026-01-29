from fastapi import FastAPI
from app.routers.router import router

app = FastAPI(title="Score API")
app.include_router(router)
