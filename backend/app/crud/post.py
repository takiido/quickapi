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
    posts = session.query(Post).filter(Post.disabled == False).all()
    return posts

def get_post(session, post_id: int):
    post = session.get(Post, post_id)
    if not post or post.disabled:
        return None
    return post

def get_posts_by_user_id(session, user_id: int):
    posts = (
        session.query(Post)
        .filter(Post.user_id == user_id)
        .filter(Post.disabled == False)
        .all()
    )
    return posts

def get_posts_by_username(session, username: str):
    posts = (
        session.query(Post)
        .join(User, Post.user_id == User.id)
        .filter(User.username == username)
        .filter(Post.disabled == False)
        .all()
    )
    return posts

