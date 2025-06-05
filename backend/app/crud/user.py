from app.models.user import User
from app.schemas.user import UserCreate, UserRead


def create_user(session, user_data: UserCreate):
    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        return None
    return user