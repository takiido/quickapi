import time

from pydantic import EmailStr, constr
from sqlmodel import SQLModel


class AuthorCreate(SQLModel):
    """
    Schema for creating a new author.
    This schema is used to validate the input data when creating a new author.
    Attributes:
        username (str): Unique username for the author, must be alphanumeric, 3-15 symbols.
        email (EmailStr): Email address of the author, must be valid.
        password (str): Password for the author, should be hashed before storing.
        full_name (str | None): Full name of the author, optional, 1-100 symbols.
        disabled (bool): Indicates if the author is disabled (e.g., banned or inactive).
        registered_at (str): Timestamp of when the author registered, in ISO format.
    """
    username: constr(
        min_length=3,
        max_length=15,
        pattern=r"^[a-zA-Z0-9_]+$",
        to_lower=True,
        strip_whitespace=True
    )
    email: EmailStr
    # ToDo: Consider hashing the password before storing it
    password: str
    full_name: constr(
        min_length=1,
        max_length=100,
    ) | None = None
    disabled: bool
    registered_at: str = int(time.time())


class AuthorRead(SQLModel):
    """
    Schema for reading author information.
    This schema is used to return author data, typically after creation or retrieval.
    Attributes:
        id (int): Unique identifier for the author.
        username (str): Unique username for the author.
        email (str): Email address of the author.
        full_name (str | None): Full name of the author, optional.
        disabled (bool): Indicates if the author is disabled (e.g., banned or inactive).
        registered_at (str): Timestamp of when the author registered, in ISO format.
    """
    id: int
    username: str
    email: str
    full_name: str | None = None
    disabled: bool
    registered_at: str


class AuthorUpdate(SQLModel):
    """
    Schema for updating author information.
    This schema is used to validate the input data when updating an author's details.
    Attributes:
        username (str | None): Unique username for the author, must be alphanumeric, 3-15 symbols.
        full_name (str | None): Full name of the author, optional, 1-100 symbols.
        email (EmailStr | None): Email address of the author, must be valid.
        disabled (bool | None): Indicates if the author is disabled (e.g., banned or inactive).
    """
    username: constr(
        min_length=3,
        max_length=15,
        pattern=r"^[a-zA-Z0-9_]+$",
        to_lower=True,
        strip_whitespace=True
    ) | None = None
    full_name: constr(
        min_length=1,
        max_length=100,
    )| None = None
    email: EmailStr | None = None
    disabled: bool | None = False