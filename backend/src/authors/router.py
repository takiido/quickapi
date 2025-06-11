from typing import List

from fastapi import APIRouter, Depends

from src.db import get_session
from src.authors import schemas, service

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
    return service.check_username_exists(session, username)


@router.post(
    "/",
    summary="Create a new author",
    response_model=schemas.AuthorPublic,
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


@router.get(
    "/",
    summary="Get all authors",
    response_model=List[schemas.AuthorPublic],
    status_code=200,
    response_description="List of all authors",
    responses={
        200: {"description": "List of authors"},
    }
)
def get_all_authors(
        session=Depends(get_session),
        active_only: bool = True
):
    """
    Route to retrieve all authors.

    - **active_only**: If True, only returns active authors (default is True)
    """
    return service.get_all_authors(session, active_only=active_only)


@router.get(
    "/me",
    summary="Get current author",
    response_model=schemas.AuthorRead,
    status_code=200,
    response_description="Current author details",
    responses={
        200: {"description": "Current author found"},
        404: {"description": "Current author not found"},
    }
)
def get_current_author(session=Depends(get_session)):
    """
    Route to retrieve the current author based on the session.

    This is typically used to get the author details of the currently authenticated user.
    """
    # ToDO: Implement logic to retrieve the current author based on the session
    return


@router.get(
    "/{author_id}",
    summary="Get author by ID",
    response_model=schemas.AuthorPublic,
    status_code=200,
    response_description="Author details",
    responses={
        200: {"description": "Author found"},
        404: {"description": "Author not found"},
    }
)
def get_author_by_id(author_id: int, session=Depends(get_session)):
    """
    Route to retrieve an author by their ID.

    - **author_id**: The ID of the author to retrieve
    """
    return service.get_author(session, author_id)


@router.get(
    "/find/{userkey}",
    summary="Get author by username or email",
    response_model=schemas.AuthorPublic,
    status_code=200,
    response_description="Author details by username or email",
    responses={
        200: {"description": "Author found"},
        404: {"description": "Author not found"},
    }
)
def get_author_by_userkey(userkey: str, session=Depends(get_session)):
    """
    Route to retrieve an author by their username or email.

    - **userkey**: The username or email of the author to retrieve
    """
    return service.get_author_by_userkey(session, userkey.lower())

@router.patch(
    "/{author_id}",
    summary="Update author details",
    response_model=schemas.AuthorPublic,
    status_code=200,
    response_description="Updated author details",
    responses={
        200: {"description": "Author updated successfully"},
        404: {"description": "Author not found"},
        422: {"description": "Validation error"},
    }
)
def update_author(author_id: int, author_data: schemas.AuthorUpdate, session=Depends(get_session)):
    """
    Route to update an author's details.

    - **author_id**: The ID of the author to update
    - **author_data**: AuthorUpdate schema instance containing the updated details
    """
    return service.update_author(session, author_id, author_data)


@router.delete(
    "/{author_id}",
    summary="Delete an author",
    status_code=204,
    response_description="Author deleted successfully",
    responses={
        204: {"description": "Author deleted successfully"},
        404: {"description": "Author not found"},
    }
)
def delete_author(author_id: int, session=Depends(get_session)):
    """
    Route to delete an author by their ID.

    - **author_id**: The ID of the author to delete
    """
    service.delete_author(session, author_id)
