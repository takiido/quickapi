from sqlmodel import select

from src.authors import models, exceptions


def check_username_exists(session, username):
    """
    Service to check if a username exists in the database.

    :param session: Database session
    :param username: Username to check
    :return: True if the username exists, False otherwise
    """
    statement = (
        select(models.Author)
        .where(models.Author.username == username.lower())
    )

    result = session.exec(statement).first()
    return result is not None


def create_author(session, author_data):
    """
    Create a new author in the database.

    :param session: Database session
    :param author_data: AuthorCreate schema instance
    :raises ValueError: If the author already exists
    """
    if check_username_exists(session, author_data.username):
        raise exceptions.UsernameAlreadyTakenException

    new_author = models.Author.model_validate(author_data)

    session.add(new_author)
    session.commit()
    session.refresh(new_author)

    return new_author
