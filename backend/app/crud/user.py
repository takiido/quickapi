from app.models.user import User
from app.schemas.user import UserCreate, UserRead


def create_user(session, user_data: UserCreate) -> User:
    if get_user_by_email(session, user_data.email):
        raise ValueError("Email already exists")
    if get_user_by_username(session, user_data.username):
        raise ValueError("Username already exists")

    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_all_users(sesssion):
    users = sesssion.query(User).all()
    return users


def get_user(session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        return None
    return user


def get_user_by_username(session, username: str):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user


def get_user_by_email(session, email: str):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    return user