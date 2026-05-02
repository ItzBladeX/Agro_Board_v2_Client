from sqlmodel import select
from app.database import get_session
from app.models import User

def get_user(id):
    with get_session() as session:
        try:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()

            return user
        
        except:
            return False

def update_user(id, name, age, gender, land_area):

    with get_session() as session:
        try:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
            if not user:
                return False

            user.name = name
            user.age = age
            user.gender = gender
            user.land_area = land_area

            session.add(user)
            print(user)
            session.commit()


            return True
        
        except  Exception as e:

            session.rollback()
            print("Update Error:", e)

            return False
        
def link_to_server(id, server_id, server_passwd):
    # if not all([user.id, user.name ,user.age, user.gender, user.land_area, server_id, server_passwd]) :
    #     return False
    pass
def delete_user(id, passwd, confirm_passwd):
    with get_session() as session:
        try:
            statement = select(User).where(User.id == id, User.passwd == passwd)
            user = session.exec(statement).one()

            session.delete(user)
            session.commit()
            return True
        
        except Exception as e:
            print("Deletion failed: ", e)
            session.rollback()
            return False

    
