from pydantic import BaseModel
import time
import calendar


class PostCreate(BaseModel):
    user_id: int
    content: str
    createdAt: str = str(calendar.timegm(time.gmtime()))
    disabled: bool = False


class PostRead(BaseModel):
    id: int
    user_id: int
    content: str
    createdAt: str | None = None

    class Config:
        orm_mode = True
