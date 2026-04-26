from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "agro_board.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=True) 