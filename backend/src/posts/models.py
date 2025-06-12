from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    """
    Model representing a post in the system.
    This model is used to store post information such as content, author,
    creation date, and status.

    Attributes:
        id (int | None): Unique identifier for the post, auto-incremented.
        author_id (int | None): Foreign key referencing the author of the post.
        content (str): Content of the post, must not be empty.
        created_at (str): Timestamp of when the post was created, in ISO format.
        disabled (bool): Indicates if the post is disabled (e.g., hidden or deleted).
    """
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Post ID, auto-incremented"
    )
    author_id: int = Field(
        foreign_key="author.id",
        nullable=False,
        description="Foreign key referencing the author of the post."
    )
    content: str = Field(
        index=True,
        nullable=False,
        description = "Content of the post, must not be empty."
    )
    disabled: bool = Field(
        default=False,
        index=True,
        nullable=False,
        description = "Indicates if the post is disabled (e.g., hidden or deleted)."
    )
    created_at: str = Field(
        nullable=False,
        description = "Timestamp of when the post was created, in ISO format."
    )


class Reply(SQLModel, table=True):
    """
    Model representing a reply to a post in the system.
    This model is used to store reply information such as content, author,
    creation date, and status.

    Attributes:
        id (int | None): Unique identifier for the reply, auto-incremented.
        post_id (int | None): Foreign key referencing the post being replied to.
        author_id (int | None): Foreign key referencing the author of the reply.
        content (str): Content of the reply, must not be empty.
        created_at (str): Timestamp of when the reply was created, in ISO format.
        disabled (bool): Indicates if the reply is disabled (e.g., hidden or deleted).
    """
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Reply ID, auto-incremented"
    )
    post_id: int = Field(
        foreign_key="post.id",
        nullable=False,
        description="Foreign key referencing the post being replied to."
    )
    author_id: int = Field(
        foreign_key="author.id",
        nullable=False,
        description="Foreign key referencing the author of the reply."
    )
    content: str = Field(
        index=True,
        nullable=False,
        description = "Content of the reply, must not be empty."
    )
    disabled: bool = Field(
        default=False,
        index=True,
        nullable=False,
        description = "Indicates if the reply is disabled (e.g., hidden or deleted)."
    )
    created_at: str = Field(
        nullable=False,
        description = "Timestamp of when the reply was created, in ISO format."
    )