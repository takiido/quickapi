from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db import init_db
from src.authors.router import router as authors_router
from src.posts.router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events."""
    on_startup()
    yield


def on_startup():
    try:
        init_db()
        print("Database schema initialized successfully.", flush=True)
    except Exception as e:
        print("Failed to initialize DB:", e, flush=True)
        raise e


app = FastAPI(
    title="QuickAPI",
    version="0.1.0",
    description="A simple FastAPI application with SQLModel and SQLite",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"message": "Hello QuickAPI"}


app.include_router(authors_router)
app.include_router(posts_router)
