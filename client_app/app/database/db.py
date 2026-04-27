from sqlmodel import SQLModel, Session, create_engine
from app.models import User

sqlite_file_name = "agro_board.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=True) 

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)