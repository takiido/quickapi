from hmac import new
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserDelete, UserPublic, UserCreate, UserRead, UserUpdate
from app.crud.user import (
    check_username_exists,
    create_user,
    delete_user,
    get_all_users,
    get_user,
    get_user_by_username_or_email,
    update_user,
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
    "/u/{identifier}",
    response_model=UserRead,
    responses={
        200: {"description": "User found"},
        400: {"description": "Invalid username or email"},
        404: {"description": "User not found"},
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

        user = get_user_by_username_or_email(session, identifier)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with identifier {identifier} not found"
            )
        return UserRead(**user.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch(
    "/{user_id}",
    response_model=UserPublic,
    summary="Update user username or full name",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Invalid input or username already exists"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def update(user_id: int, user: UserUpdate, session=Depends(get_session)):
    try:
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        if not isinstance(user_id, int):
            raise HTTPException(status_code=400, detail="User ID must be an integer")

        if user.username and check_username_exists(session, user.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        user = update_user(session, user_id, user)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found"
            )
        return UserPublic(id=user_id)
    except HTTPException as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/{user_id}",
    response_description="Delete user",
    responses={
        201: {"description": "User deleted successfully"},
        400: {"description": "Duplicate username or email"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def delete(user_id: int, user: UserDelete, session=Depends(get_session)):
    try:
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        if not isinstance(user_id, int):
            raise HTTPException(status_code=400, detail="User ID must be an integer")

        user = delete_user(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    except HTTPException as e:
        raise HTTPException(status_code=500, detail="Internal server error")
