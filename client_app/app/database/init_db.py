from sqlmodel import SQLModel
from app.database.db import engine
from app.models import *

def intit_db():
    SQLModel.metadata.create_all(engine)
intit_db()