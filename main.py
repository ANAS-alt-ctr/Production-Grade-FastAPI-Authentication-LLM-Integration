from fastapi import FastAPI
from database import connect_eng
from models import Base

from routes import auth_routes
from routes import protected_routes
from routes import llm_routes

Base.metadata.create_all(bind=connect_eng)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(llm_routes.router)