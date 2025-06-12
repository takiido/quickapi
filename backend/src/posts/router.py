from typing import List

from fastapi import APIRouter, Depends

from src.db import get_session
from src.posts import schemas, service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    summary="Create a new post",
    status_code=201,
    response_description="The newly created post",
    responses={
        201: {"description": "Post created successfully"},
        422: {"description": "Validation error"},
    }
)
def create_post(post_data: schemas.PostCreate, session=Depends(get_session)):
    """
    Route to create a new post.

    - **post_data**: PostCreate schema instance containing the post's details
    """
    return service.create_post(session, post_data)


@router.get(
    "/",
    summary="Get all posts",
    response_model=List[schemas.PostPublic],
    status_code=200,
    response_description="List of all posts",
    responses={
        200: {"description": "List of posts"},
    }
)
def get_all_posts(session=Depends(get_session)):
    """
    Route to retrieve all posts.
    """
    return service.get_all_posts(session)


@router.get(
    "/{post_id}",
    summary="Get a post by ID",
    response_model=schemas.PostPublic,
    status_code=200,
    response_description="Post details",
    responses={
        200: {"description": "Post found"},
        404: {"description": "Post not found"},
    }
)
def get_post_by_id(post_id: int, session=Depends(get_session)):
    """
    Route to retrieve a post by its ID.

    - **post_id**: Unique identifier for the post
    """
    return service.get_post(session, post_id)


@router.get(
    "/author/{author_id}",
    summary="Get posts by author ID",
    response_model=List[schemas.PostPublic],
    status_code=200,
    response_description="List of posts by author",
    responses={
        200: {"description": "Posts found"},
        404: {"description": "Author not found"},
    }
)
def get_posts_by_author(author_id: int, session=Depends(get_session)):
    """
    Route to retrieve all posts by a specific author.

    - **author_id**: ID of the author whose posts to retrieve
    """
    return service.get_posts_by_author(session, author_id)


# ToDO: This route will be enabled once Kafka is integrated to resolve usernames to IDs.
@router.get(
    "/author/{author_username}",
    include_in_schema=False,
    summary="Get posts by author username",
    response_model=List[schemas.PostPublic],
    status_code=200,
    response_description="List of posts by author username",
    responses={
        200: {"description": "Posts found"},
        404: {"description": "Author not found"},
    }
)
def get_posts_by_author_username(author_username: str, session=Depends(get_session)):
    """
    Route to retrieve all posts by a specific author using their username.

    - **author_username**: Username of the author whose posts to retrieve
    """
    return service.get_posts_by_username(session, author_username)


@router.patch(
    "/{post_id}",
    summary="Disable post",
    response_model=schemas.PostPublic,
    status_code=200,
    response_description="Updated post details",
    responses={
        200: {"description": "Post disabled successfully"},
        404: {"description": "Post not found"},
        422: {"description": "Validation error"},
    }
)
def disable_post(post_id: int, session=Depends(get_session)):
    """
    Route to disable a post by its ID.

    - **post_id**: Unique identifier for the post to disable
    """
    return service.disable_post(session, post_id)


@router.delete(
    "/{post_id}",
    summary="Delete post",
    status_code=204,
    response_description="Post deleted successfully",
    responses={
        204: {"description": "Post deleted successfully"},
        404: {"description": "Post not found"},
    }
)
def delete_post(post_id: int, session=Depends(get_session)):
    """
    Route to delete a post by its ID.

    - **post_id**: Unique identifier for the post to delete
    """
    service.delete_post(session, post_id)
