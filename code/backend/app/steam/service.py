from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Steam
from app.steam.schema import SteamCreate

def _row_to_steam(row) -> Steam:
    """
        Define -
        Entry -
        Exit -
    """
    return Steam(**row._mapping)


def create_steam(db: Session, data: SteamCreate) -> Steam:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("""
            INSERT INTO public.steam (user_id, steam_id)
            VALUES (:user_id, :steam_id)
            RETURNING *
        """),
        data.model_dump(),
    ).one()
    db.commit()
    return _row_to_steam(row)


def upsert_steam(db: Session, data: SteamCreate) -> Steam:
    row = db.execute(
        text("SELECT * FROM public.steam WHERE user_id = :user_id ORDER BY primary_id LIMIT 1"),
        data.model_dump(),
    ).one_or_none()
    if row is None:
        return create_steam(db, data)
    row = db.execute(
        text("UPDATE public.steam SET steam_id = :steam_id WHERE user_id = :user_id RETURNING *"),
        data.model_dump(),
    ).one()
    db.commit()
    return _row_to_steam(row)


def list_steam(db: Session) -> list[Steam]:
    """
        Define -
        Entry -
        Exit -
    """
    rows = db.execute(
        text("SELECT * FROM public.steam ORDER BY primary_id")
    ).all()
    return [_row_to_steam(row) for row in rows]


def get_steam(db: Session, primary_id: int) -> Steam | None:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("SELECT * FROM public.steam WHERE primary_id = :primary_id"),
        {"primary_id": primary_id},
    ).one_or_none()
    return _row_to_steam(row) if row else None


def get_steam_for_user(db: Session, user_id: int) -> Steam | None:
    row = db.execute(
        text("SELECT * FROM public.steam WHERE user_id = :user_id ORDER BY primary_id LIMIT 1"),
        {"user_id": user_id},
    ).one_or_none()
    return _row_to_steam(row) if row else None


def delete_steam(db: Session, primary_id: int) -> None:
    """
        Define -
        Entry -
        Exit -
    """
    db.execute(
        text("DELETE FROM public.steam WHERE primary_id = :primary_id"),
        {"primary_id": primary_id},
    )
    db.commit()