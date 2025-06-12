import time

from pydantic import constr
from sqlmodel import SQLModel

class PostCreate(SQLModel):
    """
    Schema for creating a new post.
    This schema is used to validate the input data when creating a new post.
    Attributes:
        content (str): Content of the post, must be 1-420 🤙 characters long.
        author_id (int): Unique identifier for the author of the post.
        created_at (str): Timestamp of when the post was created, in ISO format.
    """
    content: constr(
        min_length=1,
        max_length=420
    )
    author_id: int
    created_at: str = int(time.time())


class PostRead(SQLModel):
    """
    Schema for reading post information.
    This schema is used to return post data, typically after creation or retrieval.
    Attributes:
        id (int): Unique identifier for the post.
        content (str): Content of the post.
        author_id (int): Unique identifier for the author of the post.
        created_at (str): Timestamp of when the post was created, in ISO format.
        disabled (bool): Indicates if the post is disabled (e.g., hidden or deleted).
    """
    id: int
    content: str
    author_id: int
    created_at: str
    disabled: bool


class PostPublic(SQLModel):
    """
    Schema for public post information.
    This schema is used to return post data without sensitive information.
    Attributes:
        id (int): Unique identifier for the post.
        content (str): Content of the post.
        author_username (str): Unique username for the author of the post.
        created_at (str): Timestamp of when the post was created, in ISO format.
    """
    id: int
    content: str
    author_username: str
    created_at: str