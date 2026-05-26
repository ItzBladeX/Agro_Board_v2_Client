from sqlmodel import select, or_
from app.models import Crop, CropType
from app.database import get_session
from collections import defaultdict


import streamlit as st



def create_crop(crop):

    try:

        with get_session() as session:

            session.add(crop)
            session.commit()
            
        return {"status":True, "error_code": None, "data": None}
    
    except Exception as e:
        return {"status":False, "error_code": e, "data": None}

@st.cache_data
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

@st.cache_data()     
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


@st.cache_data
def filter_crop(user_id, name = None, prod_year_list = None, prod_year_range = None, yields = None, profits = None, sort = "Production Year"):
    try:
        conditions = [Crop.user_id == user_id] 
        if name:
            conditions.append(or_(*(Crop.name == n for n in name)))
        if yields:
            if yields[0]:
                conditions.append(Crop.crop_yield >= yields[0])
            if yields[1]:
                conditions.append(Crop.crop_yield <= yields[1])
        if prod_year_list:
            
            conditions.append(
                or_(*(
                    Crop.prod_start_year == yr for yr in prod_year_list
                    
                    ),
                    *(Crop.prod_end_year == yr for yr in prod_year_list)
                )
            )
            
        if prod_year_range:
            conditions.append(Crop.prod_start_year >= prod_year_range[0])
            conditions.append(Crop.prod_end_year <= prod_year_range[-1])
        if profits:
            if profits[0]:
                conditions.append(Crop.profit >= profits[0])
            if profits[1]:
                conditions.append(Crop.profit <= profits[1])

        with get_session() as session:
            statement = select(Crop).where(*conditions)
            crops = session.exec(statement).all()

        if sort == "Yield":
            crops = sorted(crops, 
                key=lambda crop:
                    crop.crop_yield if crop.crop_yield else float("-inf"), reverse=True)
            
        elif sort == "Profit":
            crops = sorted(crops, key=lambda crop: 
                crop.profit if crop.profit else float("-inf"), reverse=True)
        
        elif sort == "Production Year":
            crops = sorted(crops, key=lambda crop: (crop.prod_start_year, crop.prod_end_year), reverse=True)
        

        return {"status": True, "error_code": False, "data": crops}
        
    except Exception as e:
        return {"status": False, "error_code": e, "data": None}
