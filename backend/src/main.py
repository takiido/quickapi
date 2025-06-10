from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import init_db
from src.routes import author, reply, post


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


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello QuickAPI"}


app.include_router(author.router)
app.include_router(post.router)
app.include_router(reply.router)
