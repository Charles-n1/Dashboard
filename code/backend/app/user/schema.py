from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
	username: str = Field(min_length=1, max_length=256)
	email: EmailStr = Field(max_length=1024)
	password: str = Field(min_length=8, max_length=256)
	first_name: str | None = Field(default=None, max_length=256)
	last_name: str | None = Field(default=None, max_length=256)


class UserLogin(BaseModel):
	email: EmailStr = Field(max_length=1024)
	password: str = Field(min_length=8, max_length=256)


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class UserSelfUpdate(BaseModel):
	username: str | None = Field(default=None, min_length=1, max_length=256)
	email: EmailStr | None = Field(default=None, max_length=1024)
	current_password: str | None = Field(default=None, min_length=8, max_length=256)
	password: str | None = Field(default=None, min_length=8, max_length=256)
	first_name: str | None = Field(default=None, max_length=256)
	last_name: str | None = Field(default=None, max_length=256)


class UserUpdate(UserSelfUpdate):
	status: str | None = Field(default=None, min_length=1, max_length=64)
	is_admin: bool | None = None


class UserRead(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	username: str
	email: str
	first_name: str | None
	last_name: str | None
	created_at: date
	updated_at: date
	status: str
	is_admin: bool