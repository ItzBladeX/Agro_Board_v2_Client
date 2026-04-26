from sqlmodel import SQLModel, Field

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    age: int
    land_area : float | None = Field(default= None)