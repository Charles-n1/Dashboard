import os
import hmac
import hashlib
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta, timezone

import jwt
from jwt import PyJWTError
from dotenv import load_dotenv

from app.utils.style import PAGE_STYLE
from app.utils.constants import ALGORITHM

OAUTH_STATE_EXPIRE_MINUTES = 10 # TODO dans le constant


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

_expire_minutes_raw = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
if not _expire_minutes_raw:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set.")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(_expire_minutes_raw)
except ValueError:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer.")


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/details", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
def root():
    """
        Define - 
        Entry - 
        Exit - 
    """
    return """
    <html>
        <head>
            <style>
                body { font-family: sans-serif; background: #111; color: #eee; text-align: center; padding: 50px; }
                h1 { color: #4CAF50; }
            </style>
        </head>
        <body>
            <h1>Services</h1>
            <p>Discord API</p>
            <p>Steam API</p>
            <p>Weather API</p>
        </body>
    </html>
    """


def create_access_token(user_id: int) -> str:
    """
        Define - 
        Entry - 
        Exit - 
    """
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expires_at}, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
        Define - 
        Entry - 
        Exit - 
    """
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )
    if "purpose" in payload:
        raise PyJWTError("Not an access token.")
    return payload


def create_oauth_state_token(user_id: int) -> str:
    """
        Define - 
        Entry - 
        Exit - 
    """
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OAUTH_STATE_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "purpose": "oauth_state", "exp": expires_at},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_oauth_state_token(token: str) -> dict:
    """
        Define - 
        Entry - 
        Exit - 
    """
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )
    if payload.get("purpose") != "oauth_state":
        raise PyJWTError("Token is not a valid OAuth state token.")
    return payload


def verify_password(password: str, password_hash: str) -> bool:
    """
        Define - 
        Entry - 
        Exit - 
    """
    try:
        algorithm, iterations, salt_hex, digest_hex = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(candidate.hex(), digest_hex)
    except (ValueError, TypeError):
        return False