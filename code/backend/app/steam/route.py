from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.steam.steam import get_player_infos, get_player_lastgame
from app.database import Steam, User, get_db
from app.dependencies import get_current_admin, get_current_user
from app.steam.schema import SteamCreate, SteamRead
from app.steam.service import create_steam, delete_steam, get_steam, get_steam_for_user, list_steam


router = APIRouter(prefix="/steam", tags=["steam"])


@router.post("", response_model=SteamRead, status_code=status.HTTP_201_CREATED)
def create(data: SteamCreate, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """
        Define -
        Entry -
        Exit -
    """
    return create_steam(db, data)


@router.get("", response_model=list[SteamRead])
def list_all(db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return list_steam(db)


def get_my_steam(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Steam:
    steam = get_steam_for_user(db, current_user.id)
    if steam is None:
        raise HTTPException(status_code=404, detail="Steam is not connected.")
    return steam


@router.get("/me")
def me(steam: Steam = Depends(get_my_steam)):
    player = get_player_infos(steam.steam_id)
    return {
        "username": player["personaname"],
        "avatar": player["avatarfull"],
    }


@router.get("/current-game")
def current_game(steam: Steam = Depends(get_my_steam)):
    player = get_player_infos(steam.steam_id)
    return {
        "name": player.get("gameextrainfo"),
        "appid": player.get("gameid"),
    }


@router.get("/last-game")
def last_game(count: int = 1, steam: Steam = Depends(get_my_steam)):
    if count < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Count must be positive.")
    return get_player_lastgame(steam.steam_id, count)


@router.get("/{primary_id}", response_model=SteamRead)
def get(primary_id: int, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    steam = get_steam(db, primary_id)
    if steam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steam record not found.")
    return steam


@router.delete("/{primary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(primary_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """
        Define -
        Entry -
        Exit -
    """
    if get_steam(db, primary_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steam record not found.")
    delete_steam(db, primary_id)