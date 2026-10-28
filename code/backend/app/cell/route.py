from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import User, get_db
from app.dependencies import get_current_user
from app.cell.schema import CellCreate, CellRead
from app.cell.service import create_cell, delete_cell, get_cell, list_cell


router = APIRouter(prefix="/cell", tags=["cell"])


@router.post("", response_model=CellRead, status_code=status.HTTP_201_CREATED)
def create(data: CellCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return create_cell(db, data, current_user.id)


@router.get("", response_model=list[CellRead])
def list_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    return list_cell(db, current_user.id)


@router.get("/{cell_id}", response_model=CellRead)
def get(cell_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    cell = get_cell(db, cell_id, current_user.id)
    if cell is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cell record not found.")
    return cell


@router.delete("/{cell_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(cell_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        Define -
        Entry -
        Exit -
    """
    if get_cell(db, cell_id, current_user.id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cell record not found.")
    delete_cell(db, cell_id, current_user.id)