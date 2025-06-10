from sqlmodel import select
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate


def create_post(session, post_data: PostCreate) -> Post:
    post = Post(**post_data.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_all_posts(session):
    statement = (
        select(Post)
        .join(User)
        .where(
            Post.disabled == False,
            User.disabled == False
        )
    )
    posts = session.exec(statement).all()
    return posts

def get_post(session, post_id: int):
    statement = (
        select(Post)
        .join(User, Post.user_id == User.id)
        .where(
            Post.id == post_id,
            Post.disabled == False,
            User.disabled == False
        )
    )
    post = session.exec(statement).first()
    if post is None:
        return None
    return post

def get_posts_by_user_id(session, user_id: int):
    statement = (
        select(Post)
        .join(User)
        .where(
            User.id == user_id,
            Post.disabled == False,
            User.disabled == False
        )
    )
    posts = session.exec(statement).all()
    return posts

def get_posts_by_username(session, username: str):
    statement = (
        select(Post)
        .join(User)
        .where(
            User.username == username,
            Post.disabled == False,
            User.disabled == False
        )
    )
    posts = session.exec(statement).all()
    return posts

def delete_post(session, post_id: int):
    db_post = session.query(Post).get(post_id)
    if db_post is None or db_post.disabled:
        return None

    db_post.disabled = True
    session.commit()
    session.refresh(db_post)
    return db_post