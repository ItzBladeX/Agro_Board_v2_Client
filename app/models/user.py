from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None = Field(default=None)
    gender: str | None = Field(default=None)
    land_area: float | None = Field(default=None)
    passwd: str