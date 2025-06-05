from fastapi import FastAPI
from app.db import init_db, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        init_db()
        print("Database schema initialized successfully.", flush=True)
    except Exception as e:
        print("Failed to initialize DB:", e, flush=True)
        raise e

@app.get("/")
def read_root():
    return {"message": "Hello QuickAPI"}