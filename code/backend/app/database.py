"""
    database.py
    This file contains the database class and the database connection function to the PostgreSQL database.
"""

import os
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


class Discord(Base):
    __tablename__ = "discord"

    primary_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    global_name: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    avatar: Mapped[str] = mapped_column(String(256), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    hashed_token: Mapped[str] = mapped_column(String(1024), nullable=False)

class Steam(Base):
    __tablename__ = "steam"

    primary_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    steam_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

class Grid(Base):
    __tablename__ = "grid"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    columns: Mapped[int] = mapped_column(Integer, nullable=False, default=13, server_default="13")
    rows: Mapped[int] = mapped_column(Integer, nullable=False, default=6, server_default="6")


class Cell(Base):
    __tablename__ = "cell"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    grid_id: Mapped[int] = mapped_column(ForeignKey("grid.id"), nullable=False)
    widget_type: Mapped[str] = mapped_column(String(512), nullable=False)
    widget_id: Mapped[str] = mapped_column(String(128), nullable=False)
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")


class Log(Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(String(1024), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    created_on: Mapped[date] = mapped_column(Date, nullable=False)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(1024), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(256))
    last_name: Mapped[str | None] = mapped_column(String(256))
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), onupdate=func.current_date(), nullable=False)
    status: Mapped[str] = mapped_column(String(64), default="active", server_default="active", nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)


def get_db():
    """
        Define -
        Entry -
        Exit -
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()