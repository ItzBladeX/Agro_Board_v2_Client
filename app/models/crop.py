from sqlmodel import SQLModel, Field, JSON
from app.models.user import User
from datetime import date

class Crop(SQLModel, table = True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key= 'user.id')
    crop_type_id: int = Field(foreign_key= 'croptype.id')
    name: str
    prod_start_year: int 
    prod_end_year: int
    planted_date: date | None = Field(default_factory = date.today)
    harvest_date: date | None
    crop_yield: float | None 
    prod_cost: float | None
    sell_price: float | None
    profit: float | None
    notes: str | None


class CropType(SQLModel, table = True):
    __table_args__ = {'extend_existing': True}
    id : int | None = Field(default=None, primary_key=True)
    name: str = Field(unique = True, index = True)
    growth_month: int = Field(default = 0)
