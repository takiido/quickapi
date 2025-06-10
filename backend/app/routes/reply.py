from fastapi import APIRouter, Depends, HTTPException

from app.crud.reply import (
    create_reply,
    get_replies_by_post_id
)
from app.db import get_session
from app.schemas.reply import ReplyCreate, ReplyRead

router = APIRouter(prefix="/r", tags=["reply"])

@router.post(
    "/create",
    status_code=201,
    response_description="Create a new reply",
    responses={
        201: {"description": "Reply created successfully"},
        400: {"description": "Invalid reply data"},
        500: {"description": "Internal server error"},
    },
)
async def create(reply: ReplyCreate, session=Depends(get_session)):
    try:
        create_reply(session, reply)
        return {"message": "Reply created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{post_id}",
    response_model=list[ReplyRead],
    response_description="Get all replies for a post",
    responses={
        200: {"description": "List of replies"},
        400: {"description": "Invalid post ID"},
        500: {"description": "Internal server error"},
    },
)
async def get(post_id: int, session=Depends(get_session)):
    replies = get_replies_by_post_id(session, post_id)
    return replies