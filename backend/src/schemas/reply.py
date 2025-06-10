from pydantic import BaseModel
import calendar
import time


class ReplyCreate(BaseModel):
    author_id: int
    post_id: int
    content: str
    createdAt: str = str(calendar.timegm(time.gmtime()))
    disabled: bool = False


class ReplyRead(BaseModel):
    id: int
    author_id: int
    post_id: int
    content: str
    createdAt: str | None = None

    class Config:
        orm_mode = True