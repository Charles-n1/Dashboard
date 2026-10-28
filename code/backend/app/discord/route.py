from sqlalchemy.orm import Session
from app.database import User, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_admin, get_current_user
from app.discord.schema import DiscordCreate, DiscordRead, DiscordUpdate
from app.discord.service import create_discord, delete_discord, discord_exists, get_discord, get_discord_for_user, list_discord, update_discord

router = APIRouter(prefix="/discord", tags=["discord"])


@router.post("", response_model=DiscordRead, status_code=status.HTTP_201_CREATED)
def create(data: DiscordCreate, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """
        Define -
        Entry -
        Exit -
    """
    return create_discord(db, data)


@router.get("", response_model=list[DiscordRead])
def list_all(db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return list_discord(db)


@router.get("/me", response_model=DiscordRead)
def current(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
        Define -
        Entry -
        Exit -
    """
    discord_record = get_discord_for_user(db, current_user.id)
    if discord_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord is not connected.")
    return discord_record


@router.get("/{primary_id}/exists")
def exists(primary_id: int, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return {"exists": discord_exists(db, primary_id)}


@router.get("/{primary_id}", response_model=DiscordRead)
def get(primary_id: int, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    discord_record = get_discord(db, primary_id)
    if discord_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord record not found.")
    return discord_record


@router.patch("/{primary_id}", response_model=DiscordRead)
def update(primary_id: int, data: DiscordUpdate, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """
        Define -
        Entry -
        Exit -
    """
    if not discord_exists(db, primary_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord record not found.")
    return update_discord(db, primary_id, data)


@router.delete("/{primary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(primary_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin),):
    """
        Define -
        Entry -
        Exit -
    """
    if not discord_exists(db, primary_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord record not found.")
    delete_discord(db, primary_id)
