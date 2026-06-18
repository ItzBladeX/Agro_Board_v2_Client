from sqlmodel import select, or_
from app.models import Crop, CropType
from app.database import get_session
from collections import defaultdict



def create_crop(crop):

    try:

        with get_session() as session:

            session.add(crop)
            session.commit()
            
        return {"status":True, "error_code": None, "data": None}
    
    except Exception as e:
        return {"status":False, "error_code": e, "data": None}


def get_crop(user_id, crop_id=None):

    try:
        conditions = []
        if user_id:
            conditions.append(Crop.user_id == user_id)
        if crop_id:
            conditions.append(Crop.id == crop_id)
        with get_session() as session:
            statement = select(Crop).where(*conditions)
            crops = session.exec(statement).all()
        
        return {"status": True, "error_code": None, "data": crops}

    except Exception as e:
            return {"status": False, "error_code": e, "data": None}

    
def get_crop_types():
    try:
        with get_session() as session:
            crop_types = session.exec(select(CropType)).all()
            crop_def_dict = defaultdict(int)
            for crop_type in crop_types:
                crop_def_dict[crop_type.name] = crop_type.id
            
            return {"status": True, "error_code": None, "data": dict(crop_def_dict)}
          
    except Exception as e:
         return {"status": False, "error_code": e, "data": None}

def update_crop(new_crop):
    try:
        with get_session() as session:

            session.merge(new_crop)
            session.commit()

            return {"status": True, "error_code": None, "date":None}
        
    except Exception as e:
        return {"status": False, "error_code": e, "date":None}
        
def del_crop( crop_id,user_id,):
    try:
        with get_session() as session:
            statement = select(Crop).where(Crop.id == crop_id, Crop.user_id == user_id)

            crop = session.exec(statement).first()
            
            session.delete(crop)
            session.commit()

            return {"status": True, "error_code": None, "data": None}
    except Exception as e:
        {"status": False, "error_code": e, "data": None}


def drop_crops(user_id):
    try:
        with get_session() as session:
            crops = session.exec(select(Crop).where(Crop.user_id == user_id)).all()
            for crop in crops:
                session.delete(crop)

            session.commit()

            return {"status": True, "error_code": None, "data":None}
        
    except Exception as e:
        return {"status": False, "error_code": e, "data":None}



# def filter_crop(Data_Class, user_id, name = None, prod_year_list = None, prod_year_range = None, yields = None, amounts=None, profits = None, sort = "Production Year"):
#     try:
#         conditions = [Data_Class.user_id == user_id] 
#         if name:
#             conditions.append(or_(*(Data_Class.name == n for n in name)))
#         if yields:
#             if yields[0]:
#                 conditions.append(Data_Class.crop_yield >= yields[0])
#             if yields[1]:
#                 conditions.append(Data_Class.crop_yield <= yields[1])
#         if amounts:
#             if amounts[0]:
#                 conditions.append(Data_Class.amount >= amounts[0])
#             if amounts[1]:
#                 conditions.append(Data_Class.amount <= amounts[1])
        
#         if prod_year_list:
            
#             conditions.append(
#                 or_(*(
#                     Data_Class.prod_start_year == yr for yr in prod_year_list
                    
#                     ),
#                     *(Data_Class.prod_end_year == yr for yr in prod_year_list)
#                 )
#             )
            
#         if prod_year_range:
#             conditions.append(Data_Class.prod_start_year >= prod_year_range[0])
#             conditions.append(Data_Class.prod_end_year <= prod_year_range[-1])
#         if profits:
#             if profits[0]:
#                 conditions.append(Data_Class.profit >= profits[0])
#             if profits[1]:
#                 conditions.append(Data_Class.profit <= profits[1])

#         with get_session() as session:

#             statement = select(Data_Class).where(*conditions)
#             data = session.exec(statement).all()

#         if sort == "Yield":
#             data = sorted(data, 
#                 key=lambda data:
#                     data.crop_yield if data.crop_yield else float("-inf"), reverse=True)
            
#         if sort == "Amount":
#             data = sorted(data, 
#                 key=lambda data:
#                     data.amount if data.amount else float("-inf"), reverse=True)
        
#         elif sort == "Profit":
#             data = sorted(data, key=lambda data: 
#                 data.profit if data.profit else float("-inf"), reverse=True)
        
#         elif sort == "Production Year":
#             data = sorted(data, key=lambda data: (data.prod_start_year, data.prod_end_year), reverse=True)
        
#         return {"status": True, "error_code": False, "data": data}
        
#     except Exception as e:
#         return {"status": False, "error_code": e, "data": None}
