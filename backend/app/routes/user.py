from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user, get_user_by_username, get_user_by_email
from app.db import get_session

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/create",
    status_code=201,
    response_description="Create a new user",
    responses={
        201: {"description": "User created successfully"},
        400: {
            "description": "Duplicate username or email",
            "content": {
                "application/json": {"example": {"detail": "Username already exists"}}
            },
        },
        500: {"description": "Internal Server Error"},
    },
)
async def create(user: UserCreate, session=Depends(get_session)):
    try:
        create_user(session, user)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{user_id}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_by_id(user_id: int, session=Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/username/{username}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_by_username(username: str, session=Depends(get_session)):
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/email/{email}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
    },
)
async def get_by_email(email: str, session=Depends(get_session)):
    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
