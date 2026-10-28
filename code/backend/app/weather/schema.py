from pydantic import BaseModel, ConfigDict, Field


class WeatherQuery(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    model_config = ConfigDict(extra="forbid")