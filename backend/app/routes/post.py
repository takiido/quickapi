from fastapi import APIRouter, Depends, HTTPException

from app.crud.post import create_post, get_all_posts
from app.db import get_session
from app.schemas.post import PostCreate


router = APIRouter(prefix="/p", tags=["post"])


@router.post("/create", status_code=201, response_description="Create a new post")
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
)
async def get_all(session=Depends(get_session)):
    try:
        posts = get_all_posts(session)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
