from fastapi import APIRouter, Depends, HTTPException

from src.crud.post import (
    create_post,
    get_all_posts,
    get_post,
    get_posts_by_user_id,
    get_posts_by_username,
    delete_post
)
from src.db import get_session
from src.schemas.post import PostCreate, PostRead

router = APIRouter(prefix="/p", tags=["post"])


@router.post(
    "/create",
    status_code=201,
    response_description="Create a new post",
    responses={
        201: {"description": "Post created successfully"},
        400: {"description": "Invalid post data"},
        500: {"description": "Internal server error"},
    },
)
async def create(post: PostCreate, session=Depends(get_session)):
    try:
        create_post(session, post)
        return {"message": "Post created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    response_model=list[PostRead],
    response_description="Get all posts",
    responses={
        200: {"description": "List of posts"},
        500: {"description": "Internal server error"},
    },
)
async def get_all(session=Depends(get_session)):
    try:
        posts = get_all_posts(session)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{post_id}",
    summary="Retrieve post by ID",
    response_model=PostRead,
    responses={
        200: {"description": "Post found"},
        400: {"description": "Invalid post ID"},
        404: {"description": "Post not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_by_id(post_id: int, session=Depends(get_session)):
    try:
        post = get_post(session, post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/u/{user_id}",
    summary="Retrieve posts by user ID",
    response_model=list[PostRead],
    responses={
        200: {"description": "Posts found"},
        400: {"description": "Invalid user ID"},
        404: {"description": "No posts found for this user"},
        500: {"description": "Internal server error"},
    }
)
async def get_by_user_id(user_id: int, session=Depends(get_session)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    try:
        posts = get_posts_by_user_id(session, user_id)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this user")
        return posts
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/u/d/{username}",
    summary="Retrieve posts by username",
    response_model=list[PostRead],
    responses={
        200: {"description": "Posts found"},
        400: {"description": "Invalid username"},
        404: {"description": "No posts found for this user"},
        500: {"description": "Internal server error"},
    }
)
async def get_by_username(username: str, session=Depends(get_session)):
    if not username.strip():
        raise HTTPException(status_code=400, detail="Invalid username")

    try:
        posts = get_posts_by_username(session, username)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this user")
        return posts
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{post_id}",
    summary="Delete post by ID",
    response_description="Delete a post",
    responses={
        200: {"description": "Post deleted successfully"},
        400: {"description": "Invalid post ID"},
        404: {"description": "Post not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete(post_id: int, session=Depends(get_session)):
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid post ID")

    try:
        post = delete_post(session, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
