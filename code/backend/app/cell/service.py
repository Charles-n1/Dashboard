from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Cell
from app.cell.schema import CellCreate


def _row_to_cell(row) -> Cell:
    return Cell(**row._mapping)


def create_cell(db: Session, data: CellCreate, user_id: int) -> Cell:
    grid = db.execute(
        text("SELECT 1 FROM public.grid WHERE id = :grid_id AND user_id = :user_id"),
        {"grid_id": data.grid_id, "user_id": user_id},
    ).one_or_none()
    if grid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grid record not found.")

    row = db.execute(
        text("""
            INSERT INTO public.cell (grid_id, widget_type, widget_id, x, y, width, height)
            VALUES (:grid_id, :widget_type, :widget_id, :x, :y, :width, :height)
            RETURNING *
        """),
        data.model_dump(),
    ).one()
    db.commit()
    return _row_to_cell(row)


def list_cell(db: Session, user_id: int) -> list[Cell]:
    rows = db.execute(
        text("""
            SELECT cell.*
            FROM public.cell AS cell
            JOIN public.grid AS grid ON grid.id = cell.grid_id
            WHERE grid.user_id = :user_id
            ORDER BY cell.id
        """),
        {"user_id": user_id},
    ).all()
    return [_row_to_cell(row) for row in rows]


def get_cell(db: Session, cell_id: int, user_id: int) -> Cell | None:
    row = db.execute(
        text("""
            SELECT cell.*
            FROM public.cell AS cell
            JOIN public.grid AS grid ON grid.id = cell.grid_id
            WHERE cell.id = :cell_id AND grid.user_id = :user_id
        """),
        {"cell_id": cell_id, "user_id": user_id},
    ).one_or_none()
    return _row_to_cell(row) if row else None


def delete_cell(db: Session, cell_id: int, user_id: int) -> None:
    db.execute(
        text("""
            DELETE FROM public.cell AS cell
            USING public.grid AS grid
            WHERE cell.grid_id = grid.id
              AND cell.id = :cell_id
              AND grid.user_id = :user_id
        """),
        {"cell_id": cell_id, "user_id": user_id},
    )
    db.commit()
