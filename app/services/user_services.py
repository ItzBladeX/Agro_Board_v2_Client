from sqlmodel import select
from app.database import get_session
from app.models import User

def get_user_by_id(id):
    with get_session() as session:
        try:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()

            return user
        
        except:

            return False

def update_user(id, name, age, gender, passwd, land_area):

    with get_session() as session:
        try:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
            if not user:
                return False

            user.name = name
            user.age = age
            user.gender = gender
            if passwd:
                user.passwd = passwd
            user.land_area = land_area

            session.add(user)
            print(user)
            session.commit()


            return True
        
        except  Exception as e:

            session.rollback()
            print("Update Error:", e)

            return False
