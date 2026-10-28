from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Discord
from app.discord.schema import DiscordCreate, DiscordUpdate



def _row_to_discord(row) -> Discord:
    """
        Define -
        Entry -
        Exit -
    """
    return Discord(**row._mapping)


def create_discord(db: Session, data: DiscordCreate) -> Discord:
    """
        Define -
        Entry -
        Exit -
    """
    values = data.model_dump(mode="json")
    columns = ", ".join(values.keys())
    placeholders = ", ".join(f":{key}" for key in values.keys())

    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text(f"""
            INSERT INTO public.discord ({columns})
            VALUES ({placeholders})
            RETURNING *
        """),
        values,
    ).one()
    db.commit()
    return _row_to_discord(row)


def get_discord_by_external_id(db: Session, discord_id: int) -> Discord | None:
    row = db.execute(
        text("""
            SELECT *
            FROM public.discord
            WHERE id = :discord_id
        """),
        {"discord_id": discord_id},
    ).one_or_none()
    return _row_to_discord(row) if row else None


def upsert_discord(db: Session, data: DiscordCreate) -> Discord:
    """
        Define -
        Entry -
        Exit -
    """
    values = data.model_dump(mode="json")
    columns = ", ".join(values.keys())
    placeholders = ", ".join(f":{key}" for key in values.keys())
    update_clause = ", ".join(
        f"{key} = EXCLUDED.{key}" for key in values.keys() if key != "id"
    )

    row = db.execute(
        text(f"""
            INSERT INTO public.discord ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE
            SET {update_clause}
            RETURNING *
        """),
        values,
    ).one()
    db.commit()
    return _row_to_discord(row)


def update_discord(db: Session, primary_id: int, data: DiscordUpdate) -> Discord:
    """
        Define -
        Entry -
        Exit -
    """
    values = data.model_dump(exclude_unset=True, exclude_none=True)
    if not values:
        return get_discord(db, primary_id)
    set_clause = ", ".join(f"{key} = :{key}" for key in values.keys())

    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text(f"""
            UPDATE public.discord
            SET {set_clause}
            WHERE primary_id = :primary_id
            RETURNING *
        """),
        {**values, "primary_id": primary_id},
    ).one_or_none()
    db.commit()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord data not found.")
    return _row_to_discord(row)


def get_discord_for_user(db: Session, user_id: int) -> Discord | None:
    row = db.execute(
        text("""
            SELECT *
            FROM public.discord
            WHERE user_id = :user_id
            ORDER BY primary_id
            LIMIT 1
        """),
        {"user_id": user_id},
    ).one_or_none()
    return _row_to_discord(row) if row else None


def list_discord(db: Session) -> list[Discord]:
    """
        Define -
        Entry -
        Exit -
    """
    rows = db.execute(
        text("""
            SELECT *
            FROM public.discord
            ORDER BY primary_id
        """)
    ).all()
    return [_row_to_discord(row) for row in rows]


def get_discord(db: Session, primary_id: int) -> Discord:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("""
            SELECT *
            FROM public.discord
            WHERE primary_id = :primary_id
        """),
        {"primary_id": primary_id},
    ).one_or_none()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discord data not found.")
    return _row_to_discord(row)


def discord_exists(db: Session, primary_id: int) -> bool:
    """
        Define -
        Entry -
        Exit -
    """
    row = db.execute(
        text("""
            SELECT 1
            FROM public.discord
            WHERE primary_id = :primary_id
        """),
        {"primary_id": primary_id},
    ).one_or_none()
    return row is not None


def delete_discord(db: Session, primary_id: int) -> None:
    """
        Define -
        Entry -
        Exit -
    """
    get_discord(db, primary_id)  # raises 404 if it doesn't exist
    db.execute(
        text("""
            DELETE FROM public.discord
            WHERE primary_id = :primary_id
        """),
        {"primary_id": primary_id},
    )
    db.commit()