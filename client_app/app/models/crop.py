from sqlmodel import SQLModel, Field
from user import User

class Crop(SQLModel, table = True):
    id: int | None = Field(default=True, primary_key=True)
    name: str
    user_id : int = Field(foreign_key="user.id")