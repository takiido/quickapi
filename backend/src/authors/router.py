from fastapi import APIRouter

from src.authors.schemas import AuthorRead

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post(
    "/",
    summary="Create a new author",
    response_model=AuthorRead,
    status_code=201,
    description="Create a new author with the provided details. The password should be hashed before sending.",
    responses={
        201: {"description": "Author created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Author already exists"}
    }
)
def create_author(author: AuthorRead):
    print(f"Creating author: {author.username}")