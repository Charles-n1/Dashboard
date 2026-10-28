from pydantic import BaseModel, ConfigDict, field_serializer


class SteamRead(BaseModel):
    primary_id: int
    user_id: int
    steam_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("steam_id")
    def serialize_steam_id(self, value: int) -> str:
        return str(value)


class SteamCreate(BaseModel):
    user_id: int
    steam_id: int
