import time

from pydantic import EmailStr, constr
from sqlmodel import SQLModel


class AuthorCreate(SQLModel):
    username: constr(
        min_length=3,
        max_length=15,
        regex=r"^[a-zA-Z0-9_]+$",
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
    id: int
    username: str
    email: str
    full_name: str | None = None
    disabled: bool
    registered_at: str


class AuthorUpdate(SQLModel):
    username: constr(
        min_length=3,
        max_length=15,
        regex=r"^[a-zA-Z0-9_]+$",
        to_lower=True,
        strip_whitespace=True
    ) | None = None
    full_name: constr(
        min_length=1,
        max_length=100,
    )| None = None
    email: EmailStr | None = None
    disabled: bool | None = False