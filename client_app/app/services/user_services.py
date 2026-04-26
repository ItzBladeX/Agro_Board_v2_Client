from database import engine
from sqlmodel import select, Session
from models import User

def get_user_by_id(id):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()
        return user
