from sqlmodel import select
from app.models.reply import Reply
from app.schemas.reply import ReplyCreate
from app.models.author import Author
from app.models.post import Post


def create_reply(session, reply_data: ReplyCreate):
    reply = Reply(**reply_data.model_dump())
    session.add(reply)
    session.commit()
    session.refresh(reply)
    return reply


def get_replies_by_post_id(session, post_id: int):
    statement = (
        select(
            Reply
        )
        .join(Author)
        .join(Post)
        .where(
            Reply.post_id == post_id,
        Reply.disabled == False
        )
    )
    replies = session.exec(statement).all()
    return replies
