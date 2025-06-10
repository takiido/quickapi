from pydantic import BaseModel, EmailStr


class AuthorPublic(BaseModel):
    id: int


class AuthorCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None
    disabled: bool = False


class AuthorRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

    model_config = {"from_attributes": True}


class AuthorUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None

    model_config = {"from_attributes": True}


class AuthorDelete(BaseModel):
    disabled: bool | None = True

    model_config = {"from_attributes": True}

