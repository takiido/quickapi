from sqlmodel import SQLModel, Field


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    password: str = Field(nullable=False)
    full_name: str | None = Field(index=True, nullable=True)
    disabled: bool = Field(default=False, index=True, nullable=False)
    