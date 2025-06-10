from fastapi import APIRouter, Depends, HTTPException

from src.crud.reply import (
    create_reply,
    get_replies_by_post_id, delete_reply
)
from src.db import get_session
from src.schemas.reply import ReplyCreate, ReplyRead
from src.utils.validations import validate_id

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
        404: {"description": "No replies found for this post"},
        500: {"description": "Internal server error"},
    },
)
async def get(post_id: int, session=Depends(get_session)):
    validate_id(post_id, "post")

    try:
        replies = get_replies_by_post_id(session, post_id)
        if replies is None:
            raise HTTPException(status_code=404, detail="No replies found for this post")
        return replies
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{reply_id}",
    status_code=204,
    response_description="Delete a reply",
    responses={
        204: {"description": "Reply deleted successfully"},
        400: {"description": "Invalid reply ID"},
        404: {"description": "Reply not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete(reply_id: int, session=Depends(get_session)):
    validate_id(reply_id, "reply")

    try:
        deleted_reply = delete_reply(session, reply_id)
        if deleted_reply is None:
            raise HTTPException(status_code=404, detail="Reply not found")
        return {"message": "Reply deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")