from app.models.post import Post
from app.schemas.post import PostCreate


def create_post(session, post_data: PostCreate) -> Post:
    post = Post(**post_data.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_all_posts(session):
    posts = session.query(Post).filter(not Post.disabled).all()
    return posts
