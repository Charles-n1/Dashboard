from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import User, get_db
from app.dependencies import get_current_user
from app.grid.schema import GridLayoutRead, GridLayoutUpdate, GridRead
from app.grid.service import create_grid, delete_grid, get_grid, get_user_grid, list_grid, save_user_grid


router = APIRouter(prefix="/grid", tags=["grid"])


@router.post("", response_model=GridRead, status_code=status.HTTP_201_CREATED)
def create(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return create_grid(db, current_user.id)


@router.get("", response_model=list[GridRead])
def list_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return list_grid(db, current_user.id)


@router.get("/me", response_model=GridLayoutRead)
def get_current(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_grid(db, current_user.id)


@router.put("/me", response_model=GridLayoutRead)
def update_current(data: GridLayoutUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return save_user_grid(db, current_user.id, data)


@router.get("/{grid_id}", response_model=GridRead)
def get(grid_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    grid = get_grid(db, grid_id, current_user.id)
    if grid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grid record not found.")
    return grid


@router.delete("/{grid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(grid_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    if get_grid(db, grid_id, current_user.id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grid record not found.")
    delete_grid(db, grid_id, current_user.id)