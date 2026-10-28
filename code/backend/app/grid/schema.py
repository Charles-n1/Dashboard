from pydantic import BaseModel, ConfigDict, Field

from app.cell.schema import CellRead


class GridRead(BaseModel):
    id: int
    user_id: int
    columns: int = 13
    rows: int = 6

    model_config = ConfigDict(from_attributes=True)


class GridCellUpdate(BaseModel):
    widget_type: str = Field(min_length=1, max_length=512)
    widget_id: str = Field(min_length=1, max_length=128)
    x: int = Field(ge=0, le=12)
    y: int = Field(ge=0, le=77)
    width: int = Field(ge=1, le=3)
    height: int = Field(ge=1, le=3)


class GridLayoutUpdate(BaseModel):
    columns: int = Field(ge=1, le=13)
    rows: int = Field(ge=1, le=6)
    cells: list[GridCellUpdate]


class GridLayoutRead(GridRead):
    cells: list[CellRead]
