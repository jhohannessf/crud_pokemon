from fastapi import FastAPI
from config.database import init_db
from routes.endpoints import router

app = FastAPI(title="CRUD + PokéAPI Demo")

init_db()  # cria as tabelas no SQLite ao subir

app.include_router(router)