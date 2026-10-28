from pydantic import BaseModel, ConfigDict, Field


class CellRead(BaseModel):
    id: int
    grid_id: int
    widget_type: str = Field(min_length=1, max_length=512)
    widget_id: str = Field(min_length=1, max_length=128)
    x: int
    y: int
    width: int = Field(ge=1, le=3)
    height: int = Field(ge=1, le=3)

    model_config = ConfigDict(from_attributes=True)


class CellCreate(BaseModel):
    grid_id: int
    widget_type: str = Field(min_length=1, max_length=512)
    widget_id: str = Field(min_length=1, max_length=128)
    x: int
    y: int
    width: int = Field(default=1, ge=1, le=3)
    height: int = Field(default=1, ge=1, le=3)