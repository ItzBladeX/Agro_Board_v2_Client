from app.database import get_session
from app.models import User
from sqlmodel import select
import streamlit as st


def create_user(name, passwd, age, gender, land_area):
    with get_session() as session:
        try:
            user = User(name=name, passwd=passwd, age=age,gender=gender, land_area=land_area)
            session.add(user)
            session.commit()

            session.refresh(user)

            return user
        
        except Exception as e:
            print(f"DB error {e}")
            session.rollback()

            return False

def auth_user(name, passwd):
    with get_session() as session:
        statement = select(User).where(User.name == name, User.passwd == passwd)
        user = session.exec(statement).first()
        return user
    




