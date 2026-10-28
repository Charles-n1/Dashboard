from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Cell, Grid
from app.grid.schema import GridLayoutUpdate

def _row_to_grid(row) -> Grid:
    """
        Define -
        Entry -
        Exit -
    """
    grid = Grid(**row._mapping)
    if grid.columns is None:
        grid.columns = 13
    if grid.rows is None:
        grid.rows = 6
    return grid


def create_grid(db: Session, user_id: int) -> Grid:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("""
            INSERT INTO public.grid (user_id, columns, rows)
            VALUES (:user_id, 13, 6)
            RETURNING *
        """),
        {"user_id": user_id},
    ).one()
    db.commit()
    return _row_to_grid(row)


def list_grid(db: Session, user_id: int) -> list[Grid]:
    """
        Define -
        Entry -
        Exit -
    """
    rows = db.execute(
        text("SELECT * FROM public.grid WHERE user_id = :user_id ORDER BY id"),
        {"user_id": user_id},
    ).all()
    return [_row_to_grid(row) for row in rows]


def get_user_grid(db: Session, user_id: int) -> dict:
    row = db.execute(
        text("SELECT * FROM public.grid WHERE user_id = :user_id ORDER BY id LIMIT 1"),
        {"user_id": user_id},
    ).one_or_none()
    if row is None:
        row = db.execute(
            text("""
                INSERT INTO public.grid (user_id, columns, rows)
                VALUES (:user_id, 13, 6)
                RETURNING *
            """),
            {"user_id": user_id},
        ).one()
        db.commit()

    grid = _row_to_grid(row)
    cells = db.execute(
        text("SELECT * FROM public.cell WHERE grid_id = :grid_id ORDER BY y, x"),
        {"grid_id": grid.id},
    ).all()
    return {
        "id": grid.id,
        "user_id": grid.user_id,
        "columns": grid.columns if grid.columns is not None else 13,
        "rows": grid.rows if grid.rows is not None else 6,
        "cells": [Cell(**cell._mapping) for cell in cells],
    }


def save_user_grid(db: Session, user_id: int, data: GridLayoutUpdate) -> dict:
    row = db.execute(
        text("SELECT * FROM public.grid WHERE user_id = :user_id ORDER BY id LIMIT 1"),
        {"user_id": user_id},
    ).one_or_none()
    if row is None:
        row = db.execute(
            text("""
                INSERT INTO public.grid (user_id, columns, rows)
                VALUES (:user_id, :columns, :rows)
                RETURNING *
            """),
            {"user_id": user_id, "columns": data.columns, "rows": data.rows},
        ).one()
    grid = _row_to_grid(row)

    db.execute(
        text("UPDATE public.grid SET columns = :columns, rows = :rows WHERE id = :grid_id"),
        {"columns": data.columns, "rows": data.rows, "grid_id": grid.id},
    )
    db.execute(text("DELETE FROM public.cell WHERE grid_id = :grid_id"), {"grid_id": grid.id})
    for cell in data.cells:
        db.execute(
            text("""
                INSERT INTO public.cell
                    (grid_id, widget_type, widget_id, x, y, width, height)
                VALUES
                    (:grid_id, :widget_type, :widget_id, :x, :y, :width, :height)
            """),
            {"grid_id": grid.id, **cell.model_dump()},
        )
    db.commit()
    return get_user_grid(db, user_id)


def get_grid(db: Session, grid_id: int, user_id: int) -> Grid | None:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("SELECT * FROM public.grid WHERE id = :grid_id AND user_id = :user_id"),
        {"grid_id": grid_id, "user_id": user_id},
    ).one_or_none()
    return _row_to_grid(row) if row else None


def delete_grid(db: Session, grid_id: int, user_id: int) -> None:
    """
        Define -
        Entry -
        Exit -
    """
    db.execute(
        text("""
            DELETE FROM public.cell
            WHERE grid_id = :grid_id
              AND grid_id IN (
                  SELECT id FROM public.grid WHERE id = :grid_id AND user_id = :user_id
              )
        """),
        {"grid_id": grid_id, "user_id": user_id},
    )
    db.execute(
        text("DELETE FROM public.grid WHERE id = :grid_id AND user_id = :user_id"),
        {"grid_id": grid_id, "user_id": user_id},
    )
    db.commit()