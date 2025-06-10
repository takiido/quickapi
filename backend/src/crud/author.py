from sqlalchemy import select
from src.models.author import Author
from src.schemas.author import AuthorCreate, AuthorUpdate


def create_author(session, author_data: AuthorCreate) -> Author:
    if get_author_by_email(session, author_data.email):
        raise ValueError("Email already exists")
    if check_username_exists(session, author_data.username):
        raise ValueError("Username already exists")

    new_author = Author(**author_data.model_dump())
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author


def get_all_authors(session):
    statement = (
        select(Author)
        .where(Author.disabled == False)
    )
    authors = session.exec(statement).scalars().all()
    return authors


def get_author(session, author_id: int):
    statement = (
        select(Author)
        .where(
            Author.id == author_id,
            Author.disabled == False
        )
    )
    author = session.exec(statement).scalar_one_or_none()
    return author


def get_author_by_identifier(session, identifier: str):
    statement = (
        select(Author)
        .where(
            (Author.username == identifier) | (Author.email == identifier),
            Author.disabled == False
        )
    )
    author = session.exec(statement).scalar_one_or_none()
    return author


def get_author_by_email(session, email: str):
    statement = (
        select(Author)
        .where(
            Author.email == email,
            Author.disabled == False
        )
    )
    author = session.exec(statement).scalar_one_or_none()
    return author


def update_author(session, author_id: int, author: AuthorUpdate):
    statement = (
        select(Author)
        .where(
            Author.id == author_id,
            Author.disabled == False
        )
    )
    db_author = session.exec(statement).scalar_one_or_none()

    author_data = author.model_dump(exclude_unset=True)

    db_author.sqlmodel_update(author_data)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


def check_username_exists(session, username: str):
    statement = (
        select(Author)
        .where(
            Author.username == username,
            Author.disabled == False
        )
    )
    author = session.exec(statement).scalar_one_or_none()
    return author is not None


def delete_author(session, author_id: int):
    statement = (
        select(Author)
        .where(
            Author.id == author_id,
            Author.disabled == False
        )
    )
    db_author = session.exec(statement).scalar_one_or_none()
    if not db_author or db_author.disabled:
       return None
    db_author.disabled = True
    session.commit()
    session.refresh(db_author)
    return db_author
