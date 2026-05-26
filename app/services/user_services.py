from sqlmodel import select
from app.database import get_session
from app.models import User


def get_user(id):
    try:
        with get_session() as session:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
            return user
        
    except:
        return False

def update_user(id, name, age, gender, land_area):

    try:
        with get_session() as session:
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


            return {"status": True, "error_code": None, "data": None}
        
    except  Exception as e:

        return {"status": True, "error_code": None, "data": None}
        
def link_to_server(id, server_id, server_passwd):
    # if not all([user.id, user.name ,user.age, user.gender, user.land_area, server_id, server_passwd]) :
    #     return False
    pass

def del_user(id, passwd):
    try:
        with get_session() as session:
            statement = select(User).where(User.id == id, User.passwd == passwd)
            user = session.exec(statement).first()

            session.delete(user)
            session.commit()
        

        return {"status": True, "error_code": None, "data": None}
        
    except Exception as e:
        return {"status": False, "error_code": e, "data": None}

    
