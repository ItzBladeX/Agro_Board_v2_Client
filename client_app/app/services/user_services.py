from sqlmodel import select
from app.database import get_session
from app.models import User

def get_user_by_id(id):
    with get_session() as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()
        return user
