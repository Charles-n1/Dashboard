from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.database import User, get_db
from app.dependencies import get_current_admin, get_current_user
from app.user.schema import Token, UserCreate, UserLogin, UserRead, UserSelfUpdate, UserUpdate
from app.user.service import authenticate_user, create_user, delete_user, get_user, list_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(data: UserCreate, db: Session = Depends(get_db)):
	"""
		Define -
		Entry -
		Exit -
	"""
	return create_user(db, data)


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
	"""
		Define -
		Entry -
		Exit -
	"""
	access_token = authenticate_user(db, str(data.email), data.password)
	return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def current_user(current_user: User = Depends(get_current_user)):
	"""
		Define -
		Entry -
		Exit -
	"""
	return current_user


@router.patch("/me", response_model=UserRead)
def update_current_user(data: UserSelfUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	"""
		Define -
		Entry -
		Exit -
	"""
	return update_user(db, current_user.id, data, require_current_password=True)


@router.get("", response_model=list[UserRead])
def list_all(db: Session = Depends(get_db), _admin: User = Depends(get_current_admin),):
	"""
		Define -
		Entry -
		Exit -
	"""
	return list_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get(user_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
	"""
		Define -
		Entry -
		Exit -
	"""
	return get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
	"""
		Define -
		Entry -
		Exit -
	"""
	return update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
	"""
		Define -
		Entry -
		Exit -
	"""
	delete_user(db, user_id)
