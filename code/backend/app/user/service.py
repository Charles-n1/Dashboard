import hashlib
import secrets
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import User
from app.user.schema import UserCreate, UserUpdate
from app.auth.auth import create_access_token, verify_password


def hash_password(password: str) -> str:
	"""
		Define -
		Entry -
		Exit -
	"""
	salt = secrets.token_bytes(16)
	digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
	return f"pbkdf2_sha256$600000${salt.hex()}${digest.hex()}"


def normalize_email(email: str) -> str:
	"""
		Define -
		Entry -
		Exit -
	"""
	return email.lower()


def _row_to_user(row) -> User:
	"""
		Define -
		Entry -
		Exit -
	"""
	return User(**dict(row._mapping))


def create_user(db: Session, data: UserCreate) -> User:
	"""
		Define -
		Entry -
		Exit -
	"""
	try:
		row = db.execute(
			text("""
				INSERT INTO public.user
					(password_hash,
					username,
					email,
					first_name,
					last_name)
				VALUES
					(:password_hash,
					:username,
					:email,
					:first_name,
					:last_name)
				RETURNING *
			"""),
			{
				"password_hash": hash_password(data.password),
				"username": data.username,
				"email": str(data.email),
				"first_name": data.first_name,
				"last_name": data.last_name,
			},
		).one()
		db.commit()
	except IntegrityError as exc:
		db.rollback()
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already taken.",) from exc
	return _row_to_user(row)


def list_users(db: Session) -> list[User]:
	"""
		Define -
		Entry -
		Exit -
	"""
	rows = db.execute(text(
        "SELECT * FROM public.user ORDER BY id")).all()
	return [_row_to_user(r) for r in rows]


def get_user(db: Session, user_id: int) -> User:
	"""
		Define -
		Entry -
		Exit -
	"""
	row = db.execute(
		text("SELECT * FROM public.user WHERE id = :id"),
		{"id": user_id}
    ).one_or_none()
	if row is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
	return _row_to_user(row)


def authenticate_user(db: Session, email: str, password: str) -> str:
	"""
		Define -
		Entry -
		Exit -
	"""
	row = db.execute(
		text("SELECT * FROM public.user WHERE lower(email) = :email"),
		{"email": normalize_email(email)},
	).one_or_none()
	if row is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

	user = _row_to_user(row)
	if not verify_password(password, user.password_hash) or user.status != "active":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

	return create_access_token(user.id)


def _ensure_available(db: Session, username: str, email: str, exclude_id: int) -> None:
	"""
		Define -
		Entry -
		Exit -
	"""
	row = db.execute(
		text("""
			SELECT 1 FROM public.user
			WHERE (username = :username OR lower(email) = :email) AND id != :exclude_id
			LIMIT 1
		"""),
		{"username": username, "email": normalize_email(email), "exclude_id": exclude_id},
	).one_or_none()
	if row is not None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already taken.")


def update_user(
	db: Session,
	user_id: int,
	data: UserUpdate,
	*,
	require_current_password: bool = False,
) -> User:
	"""
		Define -
		Entry -
		Exit -
	"""
	user = get_user(db, user_id)
	values = data.model_dump(exclude_unset=True)
	current_password = values.pop("current_password", None)
	if values.get("password") is not None and require_current_password:
		if current_password is None:
			raise HTTPException(
				status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
				detail="Current password is required to change the password.",
			)
		if not verify_password(current_password, user.password_hash):
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Current password is incorrect.",
			)

	if "email" in values:
		values["email"] = normalize_email(str(values["email"]))
	if "username" in values or "email" in values:
		_ensure_available(db, values.get("username", user.username), values.get("email", user.email), user_id)
	if values.get("password") is not None:
		values["password_hash"] = hash_password(values.pop("password"))
	else:
		values.pop("password", None)

	try:
		row = db.execute(
			text("""
				UPDATE public.user
				SET username = :username,
					email = :email,
					first_name = :first_name,
					last_name = :last_name,
					password_hash = :password_hash,
					status = :status,
					is_admin = :is_admin,
					updated_at = :updated_at
				WHERE id = :user_id
				RETURNING *
			"""),
			{
				"username": values.get("username", user.username),
				"email": values.get("email", user.email),
				"first_name": values.get("first_name", user.first_name),
				"last_name": values.get("last_name", user.last_name),
				"password_hash": values.get("password_hash", user.password_hash),
				"status": values.get("status", user.status),
				"is_admin": values.get("is_admin", user.is_admin),
				"updated_at": date.today(),
				"user_id": user_id,
			},
		).one()
		db.commit()
	except IntegrityError as exc:
		db.rollback()
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Username or email already taken."
		) from exc
	return _row_to_user(row)


def delete_user(db: Session, user_id: int) -> None:
	"""
		Define -
		Entry -
		Exit -
	"""
	get_user(db, user_id)
	db.execute(
		text("""
			DELETE FROM public.cell
			WHERE grid_id IN (
				SELECT id FROM public.grid WHERE user_id = :id
			)
		"""),
		{"id": user_id},
	)
	for table in ("grid", "discord", "steam", "log"):
		db.execute(
			text(f'DELETE FROM public."{table}" WHERE user_id = :id'),
			{"id": user_id},
		)
	db.execute(text("DELETE FROM public.user WHERE id = :id"), {"id": user_id})
	db.commit()