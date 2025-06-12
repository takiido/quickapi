from sqlmodel import select

from src.posts import models, exceptions
from src.authors.models import Author


def create_post(session, post_data):
    """
    Create a new post in the database.

    :param session: Database session
    :param post_data: PostCreate schema instance
    :raises ValueError: If the post already exists
    """
    new_post = models.Post.model_validate(post_data)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


def get_all_posts(session) -> list[models.Post]:
    """
    Retrieve all posts from the database.

    :param session: Database session
    :return: List of PostPublic schema instances
    """
    statement = (
        select(
            models.Post.id,
            models.Post.content,
            Author.username.label("author_username"),
            models.Post.created_at

        )
        .join(Author)
        .where(models.Post.disabled == False))
    posts = session.exec(statement).all()

    return posts


def get_post(session, post_id: int) -> models.Post:
    """
    Retrieve a post by ID from the database.

    :param session: Database session
    :param post_id: Unique identifier for the post
    :return: PostRead schema instance
    """
    statement = (
        select(
            models.Post.id,
            models.Post.content,
            Author.username.label("author_username"),
            models.Post.created_at

        )
        .join(Author)
        .where(
            models.Post.disabled == False,
            models.Post.id == post_id
        )
    )

    post = session.exec(statement).first()

    if not post:
        raise exceptions.PostNotFoundException

    return post


def get_posts_by_author(session, author_id: int) -> list[models.Post]:
    """
    Retrieve all posts by a specific author.

    :param session: Database session
    :param author_id: Unique identifier for the author
    :return: List of PostRead schema instances
    """
    statement = (
        select(
            models.Post.id,
            models.Post.content,
            Author.username.label("author_username"),
            models.Post.created_at

        )
        .join(Author)
        .where(
            models.Post.disabled == False,
            models.Post.author_id == author_id
        )
    )

    posts = session.exec(statement).all()

    if not posts:
        raise exceptions.PostNotFoundException

    return posts


def get_posts_by_username(session, username: str) -> list[models.Post]:
    """
    Retrieve all posts by a specific author's username.

    :param session: Database session
    :param username: Username of the author
    :return: List of PostRead schema instances
    """
    statement = (
        select(
            models.Post.id,
            models.Post.content,
            Author.username.label("author_username"),
            models.Post.created_at

        )
        .join(Author)
        .where(
            models.Post.disabled == False,
            Author.username == username.lower()
        )
    )

    posts = session.exec(statement).all()

    if not posts:
        raise exceptions.PostNotFoundException

    return posts


def disable_post(session, post_id: int) -> models.Post:
    """
    Disable a post by setting its 'disabled' flag to True.

    :param session: Database session
    :param post_id: Unique identifier for the post
    :return: PostRead schema instance of the disabled post
    :raises ValueError: If the post does not exist
    """
    post = get_post(session, post_id)
    post.disabled = True

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def delete_post(session, post_id: int):
    """
    Delete a post from the database.

    :param session: Database session
    :param post_id: Unique identifier for the post
    :raises ValueError: If the post does not exist
    """
    post = get_post(session, post_id)

    session.delete(post)
    session.commit()

    return {"deleted": True, "message": "Post deleted successfully"}
