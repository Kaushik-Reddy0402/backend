from sqlmodel import SQLModel, Field

from sqlmodel import Field, SQLModel

class Details(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    emp_id: int
    file_path: str | None = None

