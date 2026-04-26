from sqlmodel import SQLModel
from .db import engine
from models import *

def intit_db():
    SQLModel.metadata.create_all(engine)
intit_db()