from sqlmodel import SQLModel, Field


class Author(SQLModel, table=True):
    """
    Model representing an author in the system.
    This model is used to store author information such as username, email,
    password, full name, and registration details.
    Attributes:
        id (int | None): Unique identifier for the author, auto-incremented.
        username (str): Unique username for the author, must be alphanumeric.
        email (str): Email address of the author, must be unique.
        password (str): Password for the author, should be hashed before storing.
        full_name (str | None): Full name of the author, optional.
        disabled (bool): Indicates if the author is disabled (e.g., banned or inactive).
        registered_at (str): Timestamp of when the author registered, in ISO format.
    """
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Author ID"
    )
    username: str = Field(
        index=True,
        unique=True,
        nullable=False,
        description="Username of the author, must be unique and alphanumeric"
    )
    email: str = Field(
        index=True,
        nullable=False, description="Email address of the author"
    )
    # ToDO: Consider hashing the password before storing it
    password: str = Field(
        nullable=False,
        description="Literally the password, should be hashed before storing"
    )
    full_name: str | None = Field(
        index=True,
        nullable=True,
        description="Full name of the author, optional"
    )
    # ToDo: set default to True after implementing email verification
    disabled: bool = Field(
        default=False,
        index=True,
        nullable=False,
        description="Indicates if the author is disabled (e.g., banned or inactive)"
    )
    registered_at: str = Field(
        nullable=False,
        description="Timestamp of when the author registered (in ISO format)"
    )
