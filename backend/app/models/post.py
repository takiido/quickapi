from sqlmodel import SQLModel, Field
from sqlalchemy import Boolean


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int | None = Field(default=None, foreign_key="author.id")
    content: str = Field(index=True, nullable=False)
    createdAt: str = Field(index=True, nullable=False)
    disabled: bool = Field(
        default=False,
        sa_type=Boolean,
        nullable=False,
        index=True,
    )
