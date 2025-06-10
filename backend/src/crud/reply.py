from sqlmodel import select
from src.models.reply import Reply
from src.schemas.reply import ReplyCreate
from src.models.author import Author
from src.models.post import Post


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


def delete_reply(session, reply_id: int):
    statement = (
        select(Reply)
        .where(
            Reply.id == reply_id,
            Reply.disabled == False
        )
    )
    db_reply = session.exec(statement).first()

    if not db_reply:
        raise ValueError("Reply not found or already deleted")

    db_reply.disabled = True
    session.add(db_reply)
    session.commit()
    session.refresh(db_reply)
    return db_reply