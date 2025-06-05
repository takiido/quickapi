from sqlmodel import create_engine, Session, SQLModel
import os

db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@quickapi-postgres:5432/quickapi"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session