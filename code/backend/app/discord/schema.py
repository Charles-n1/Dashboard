from pydantic import BaseModel, Field, ConfigDict, field_serializer

class DiscordCreate(BaseModel):
    id: int  # not the primary key if, just the id gotten from discord, the id of discord, the discord id -Kronk
    user_id: int
    username: str = Field(min_length=1, max_length=256)
    global_name: str = Field(default="", max_length=256)
    email: str = Field(min_length=1, max_length=256)
    avatar: str = Field(default="", max_length=256)
    hashed_token: str = Field(min_length=1, max_length=1024)


class DiscordUpdate(BaseModel):
    user_id: int | None = None
    username: str | None = Field(default=None, min_length=1, max_length=256)
    global_name: str | None = Field(default=None, min_length=1, max_length=256)
    email: str | None = Field(default=None, min_length=1, max_length=256)
    avatar: str | None = Field(default=None, min_length=1, max_length=256)


class DiscordRead(BaseModel):
    primary_id: int
    id: int
    user_id: int
    username: str
    global_name: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, value: int) -> str:
        return str(value)