from sqlmodel import select, or_

from src.authors import models, exceptions


def check_username_exists(session, username, internal: bool = False):
    """
    Service to check if a username exists in the database.

    :param session: Database session
    :param username: Username to check
    :param internal: If True, returns a boolean; if False,
    raises an exception if not found
    :return: If internal is True, returns True if exists, False otherwise;
        if False, returns a dict with existence status
    """
    statement = (
        select(models.Author)
        .where(models.Author.username == username.lower())
    )

    result = session.exec(statement).first()

    if internal:
        if result is not None:
            return True
        return False

    if result is not None:
        return {"exists": True, "message": "Username exists"}

    raise exceptions.UsernameNotFoundException


def create_author(session, author_data):
    """
    Create a new author in the database.

    :param session: Database session
    :param author_data: AuthorCreate schema instance
    :raises ValueError: If the author already exists
    """
    if check_username_exists(session, author_data.username, internal=True):
        raise exceptions.UsernameAlreadyTakenException

    new_author = models.Author.model_validate(author_data)

    session.add(new_author)
    session.commit()
    session.refresh(new_author)

    return new_author


def get_all_authors(session, active_only: bool = True) -> list[models.Author]:
    """
    Retrieve all authors from the database.

    :param session: Database session
    :param active_only: If True, only return active authors (not disabled)
    :return: List of AuthorRead schema instances
    """
    statement = select(models.Author)
    if active_only:
        statement = statement.where(models.Author.disabled == False)

    authors = session.exec(statement).all()

    return authors


def get_author(session, author_id: int) -> models.Author:
    """
    Retrieve an author by ID from the database.

    :param session: Database session
    :param author_id: ID of the author to retrieve
    :return: AuthorRead schema instance
    :raises ValueError: If the author does not exist
    """
    statement = (
        select(models.Author)
        .where(models.Author.id == author_id)
    )
    author = session.exec(statement).first()

    if author is None:
        raise exceptions.AuthorNotFoundException

    return author


def get_author_by_userkey(session, userkey: str) -> models.Author:
    """
    Retrieve an author by userkey from the database.

    :param session: Database session
    :param userkey: Userkey of the author to retrieve
    :return: AuthorRead schema instance
    :raises ValueError: If the author does not exist
    """
    statement = (
        select(models.Author)
        .where(
            or_(
                models.Author.username == userkey.lower(),
                models.Author.email == userkey.lower()
            )
        )
    )

    author = session.exec(statement).first()

    if author is None:
        raise exceptions.AuthorNotFoundException

    return author


def update_author(session, author_id: int, author_data) -> models.Author:
    """
    Update an existing author's information in the database.

    :param session: Database session
    :param author_id: ID of the author to update
    :param author_data: AuthorUpdate schema instance with updated data
    :return: Updated AuthorRead schema instance
    :raises ValueError: If the author does not exist
        or if the username is already taken
    """
    author = get_author(session, author_id)

    data = author_data.model_dump(exclude_unset=True)
    for (key, value) in data.items():
        setattr(author, key, value)

    session.add(author)
    session.commit()
    session.refresh(author)

    return author


def delete_author(session, author_id: int):
    """
    Delete an author from the database.

    :param session: Database session
    :param author_id: ID of the author to delete
    :raises ValueError: If the author does not exist
    """
    author = get_author(session, author_id)

    session.delete(author)
    session.commit()

    return {"deleted": True, "message": f"Author deleted successfully"}
