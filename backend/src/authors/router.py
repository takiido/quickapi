from fastapi import APIRouter, Depends

from src.db import get_session
from src.authors import schemas, service, exceptions

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get(
    "/check-username/{username}",
    status_code=200,
    summary="Check if a username exists",
    response_description="Check if a username exists in the database",
    responses={
        200: {"description": "Username exists"},
        404: {"description": "Username does not exist"},
    }
)
def check_username(username: str, session=Depends(get_session)):
    """
    Route to check if a username exists in the database.

    - **username**: The username to check
    """
    if service.check_username_exists(session, username):
        return {"exists": True, "message": "Username exists"}
    raise exceptions.UsernameNotFoundException


@router.post(
    "/",
    summary="Create a new author",
    response_model=schemas.AuthorRead,
    status_code=201,
    response_description="The newly created author",
    responses={
        201: {"description": "Author created successfully"},
        409: {"description": "Author already exists"},
        422: {"description": "Validation error"},
    }
)
def register_author(author_data: schemas.AuthorCreate, session=Depends(get_session)):
    """
    Route to register a new author.

    - **author_data**: AuthorCreate schema instance containing the author's details
    """
    return service.create_author(session, author_data)