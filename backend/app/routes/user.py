from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.crud.user import (
    create_user,
    get_all_users,
    get_user,
    get_user_by_username,
    get_user_by_email,
)
from app.db import get_session

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/create",
    status_code=201,
    response_description="Create a new user",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Duplicate username or email"},
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
    "/",
    response_model=list[UserRead],
    response_description="Get all users",
    responses={
        200: {"description": "List of users"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_all(session=Depends(get_session)):
    try:
        users = get_all_users(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/{user_id}",
    summary="Retrieve user by ID",
    response_model=UserRead,
    responses={
        200: {"description": "User found"},
        400: {"description": "Invalid user ID"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_by_id(user_id: int, session=Depends(get_session)):
    try:
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        if not isinstance(user_id, int):
            raise HTTPException(status_code=400, detail="User ID must be an integer")
        
        user = get_user(session, user_id)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found"
            )
        return UserRead(**user.dict())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database session error")


@router.get(
    "/username/{username}",
    response_model=UserRead,
    responses={
        200: {"description": "User found"},
        400: {"description": "Invalid username"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_by_username(username: str, session=Depends(get_session)):
    try:
        if not username or len(username) < 3:
            raise HTTPException(status_code=400, detail="Invalid username")
        if not username.isalnum():
            raise HTTPException(status_code=400, detail="Username must be alphanumeric")
        if len(username) > 50:
            raise HTTPException(status_code=400, detail="Username too long")
        if not username[0].isalpha():
            raise HTTPException(status_code=400, detail="Username must start with a letter")
        
        user = get_user_by_username(session, username)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with username {username} not found"
                )
        return UserRead(**user.dict())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/email/{email}",
    response_model=UserRead,
    responses={
        200: {"description": "User found"},
        400: {"description": "Invalid email"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_by_email(email: str, session=Depends(get_session)):
    try:
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            raise HTTPException(status_code=400, detail="Invalid email format")
        if len(email) > 254:
            raise HTTPException(status_code=400, detail="Email too long")
        if not email.split("@")[0].isalnum():
            raise HTTPException(status_code=400, detail="Email local part must be alphanumeric")
        
        user = get_user_by_email(session, email)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with email {email} not found")
        return UserRead(**user.dict())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
