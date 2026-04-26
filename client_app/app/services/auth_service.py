from database import engine
from models import User
from sqlmodel import Session, select


def signup_user(name, passwd, age, land_area):
    with Session(engine) as session:
        try:
            user = User(name=name, passwd=passwd, age=age, land_area=land_area)
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            print(f"DB error {e}")
            session.rollback()
            return False

def login_user(name, passwd):
    with Session(engine) as session:
        statement = select(User).where(User.name == name, User.passwd == passwd)
        user = session.exec(statement).first()
        return user



