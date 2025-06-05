from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate
from app.crud.user import create_user as create_user_crud, get_user
from app.db import get_session

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create")
async def create_user(user: UserCreate, session = Depends(get_session)):
    return await create_user_crud(session, user)

@router.get("/{user_id}")
async def get_user_by_id(user_id: int, session = Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user