
from sqlmodel import select, or_
from app.models import Livestock, LivestockType
from app.database import get_session
from collections import defaultdict

def create_livestock(livestock:Livestock):
    try:
        with get_session() as session:
            session.add(livestock)
            session.commit()
            
        return {"status":True, "error_code": None, "data": None}
    
    except Exception as e:
        return {"status":False, "error_code": e, "data": None}

def get_livestock(user_id, livestock_id=None):

    try:
        conditions = []
        if user_id:
            conditions.append(Livestock.user_id == user_id)
        if livestock_id:
            conditions.append(Livestock.id == livestock_id)
        with get_session() as session:
            statement = select(Livestock).where(*conditions)
            crops = session.exec(statement).all()
        
        return {"status": True, "error_code": None, "data": crops}

    except Exception as e:
            return {"status": False, "error_code": e, "data": None}

def get_livestock_types():
    try:
        with get_session() as session:
            crop_types = session.exec(select(LivestockType)).all()
            crop_def_dict = defaultdict(int)
            for crop_type in crop_types:
                crop_def_dict[crop_type.name] = crop_type.id
            
            return {"status": True, "error_code": None, "data": dict(crop_def_dict)}
          
    except Exception as e:
         return {"status": False, "error_code": e, "data": None}

def update_livestock(new_livestock:Livestock):
    try:
        with get_session() as session:

            session.merge(new_livestock)
            session.commit()

            return {"status": True, "error_code": None, "date":None}
        
    except Exception as e:
        return {"status": False, "error_code": e, "date":None}
    
    


def del_livestock(livestock_id,user_id,):
    try:
        with get_session() as session:
            statement = select(Livestock).where(Livestock.id == livestock_id, Livestock.user_id == user_id)

            crop = session.exec(statement).first()
            
            session.delete(crop)
            session.commit()

            return {"status": True, "error_code": None, "data": None}
    except Exception as e:
        {"status": False, "error_code": e, "data": None}

def drop_livestock(user_id):
    try:
        with get_session() as session:
            crops = session.exec(select(Livestock).where(Livestock.user_id == user_id)).all()
            for crop in crops:
                session.delete(crop)

            session.commit()

            return {"status": True, "error_code": None, "data":None}
        
    except Exception as e:
        return {"status": False, "error_code": e, "data":None}