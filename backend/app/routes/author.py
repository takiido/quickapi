from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorDelete, AuthorPublic, AuthorCreate, AuthorRead, AuthorUpdate
from app.crud.author import (
    check_username_exists,
    create_author,
    delete_author,
    get_all_authors,
    get_author,
    get_author_by_identifier,
    update_author,
)
from app.db import get_session
from app.utils.validations import validate_id

router = APIRouter(prefix="/a", tags=["author"])


@router.post(
    "/create",
    status_code=201,
    response_description="Create a new author",
    responses={
        201: {"description": "Author created successfully"},
        400: {"description": "Duplicate username or email"},
        500: {"description": "Internal Server Error"},
    },
)
async def create(author: AuthorCreate, session=Depends(get_session)):
    try:
        create_author(session, author)
        return {"message": "Author created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/",
    response_model=list[AuthorRead],
    response_description="Get all authors",
    responses={
        200: {"description": "List of authors"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_all(session=Depends(get_session)):
    try:
        authors = get_all_authors(session)
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{author_id}",
    summary="Retrieve author by ID",
    # response_model=AuthorRead,
    responses={
        200: {"description": "Author found"},
        400: {"description": "Invalid author ID"},
        404: {"description": "Author not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_by_id(author_id: int, session=Depends(get_session)):
    try:
        validate_id(author_id, "author")

        author = get_author(session, author_id)
        if author is None:
            raise HTTPException(status_code=404, detail=f"Author not found")
        return AuthorRead.model_validate(author)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/ident/{identifier}",
    response_model=AuthorRead,
    responses={
        200: {"description": "Author found"},
        400: {"description": "Invalid username or email"},
        404: {"description": "Author not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_by_username_or_email(identifier: str, session=Depends(get_session)):
    try:
        if not identifier or len(identifier) < 3:
            raise HTTPException(status_code=400, detail="Invalid username or email")
        if "@" in identifier:
            if "@" not in identifier or "." not in identifier.split("@")[-1]:
                raise HTTPException(status_code=400, detail="Invalid email format")
            if len(identifier) > 254:
                raise HTTPException(status_code=400, detail="Email too long")
            if not identifier.split("@")[0].isalnum():
                raise HTTPException(
                    status_code=400, detail="Email local part must be alphanumeric"
                )
        else:
            if not identifier.isalnum():
                raise HTTPException(
                    status_code=400, detail="Username must be alphanumeric"
                )
            if len(identifier) > 50:
                raise HTTPException(status_code=400, detail="Username too long")
            if not identifier[0].isalpha():
                raise HTTPException(
                    status_code=400, detail="Username must start with a letter"
                )

        author = get_author_by_identifier(session, identifier)
        if not author:
            raise HTTPException(
                status_code=404, detail=f"Author with identifier {identifier} not found"
            )
        return AuthorRead(**author.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/{author_id}",
    response_model=AuthorPublic,
    summary="Update author username or full name",
    responses={
        200: {"description": "Author updated successfully"},
        400: {"description": "Invalid input or username already exists"},
        404: {"description": "Author not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def update(author_id: int, author: AuthorUpdate, session=Depends(get_session)):
    try:
        if author_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid author ID")
        if not isinstance(author_id, int):
            raise HTTPException(status_code=400, detail="Author ID must be an integer")

        if author.username and check_username_exists(session, author.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        author = update_author(session, author_id, author)
        if not author:
            raise HTTPException(
                status_code=404, detail=f"Author with ID {author_id} not found"
            )
        return AuthorPublic(id=author_id)
    except HTTPException as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/{author_id}",
    response_description="Delete author",
    responses={
        201: {"description": "Author deleted successfully"},
        400: {"description": "Duplicate username or email"},
        404: {"description": "Author not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def delete(author_id: int, author: AuthorDelete, session=Depends(get_session)):
    try:
        if author_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid author ID")
        if not isinstance(author_id, int):
            raise HTTPException(status_code=400, detail="Author ID must be an integer")

        author = delete_author(session, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        return {"message": "Author deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=500, detail="Internal server error")
