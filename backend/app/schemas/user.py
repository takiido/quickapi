from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: int


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None
    disabled: bool = False


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None

    model_config = {"from_attributes": True}
