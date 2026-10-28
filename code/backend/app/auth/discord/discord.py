import os
import hashlib
import httpx
from fastapi import APIRouter, Depends, Response, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from jwt import PyJWTError
from sqlalchemy.orm import Session

from app.auth.auth import create_oauth_state_token, decode_access_token, decode_oauth_state_token
from app.database import get_db
from app.discord.schema import DiscordCreate
from app.discord.service import upsert_discord

from app.utils.constants import HTTP_TIMEOUT

load_dotenv()

router = APIRouter(prefix="/auth/discord", tags=["discord"])


@router.get("")
def discord_status():
    """
        Define -
        Entry -
        Exit -
    """
    return {"service": "discord", "status": "implemented"}


@router.get("/login")
async def discord_login(token: str | None = None) -> Response:
    """
        Define -
        Entry -
        Exit -
    """
    client_id = os.getenv("DISCORD_CLIENT_ID")
    redirect_uri = os.getenv("DISCORD_REDIRECT_URI")
    if not client_id or not redirect_uri:
        raise HTTPException(status_code=500, detail="Discord OAuth configuration is missing.")

    url = (
        "https://discord.com/oauth2/authorize?"
        f"client_id={client_id}&"
        "response_type=code&"
        f"redirect_uri={redirect_uri}&"
        "scope=identify"
    )

    if token:
        try:
            user_id = int(decode_access_token(token)["sub"])
        except (KeyError, TypeError, ValueError, PyJWTError) as exc:
            raise HTTPException(status_code=401, detail="Invalid login session.") from exc

        state = create_oauth_state_token(user_id)
        url += f"&state={state}"

    return Response(status_code=status.HTTP_302_FOUND, headers={"Location": url})


@router.get("/callback")
async def discord_callback(request: Request, db: Session = Depends(get_db)):
    """
        Define -
        Entry -
        Exit -
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided.")

    state = request.query_params.get("state")
    if not state:
        raise HTTPException(status_code=401, detail="Login is required before connecting Discord.")

    try:
        user_id = int(decode_oauth_state_token(state)["sub"])
    except (KeyError, TypeError, ValueError, PyJWTError) as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired login session.") from exc

    data = {"client_id": os.getenv("DISCORD_CLIENT_ID"),
            "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        token_response = await client.post(
            "https://discord.com/api/oauth2/token",
            data=data,
            headers=headers,
        )

    if token_response.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to exchange Discord authorization code.")

    try:
        access_token = token_response.json().get("access_token")
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Unexpected response from Discord.") from exc

    if not access_token:
        raise HTTPException(status_code=502, detail="Unable to retrieve Discord user data.")

    headers = {"Authorization": f"Bearer {access_token}"}
    headers = {"Authorization": "Bearer " + access_token}
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers=headers,
        )

    if user_response.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to retrieve Discord user data.")

    discord_payload = user_response.json()
    user_data = DiscordCreate(id=int(discord_payload["id"]),
        user_id=user_id,
        username=discord_payload["username"],
        global_name=discord_payload.get("global_name") or discord_payload["username"],
        email=discord_payload.get("email") or f"{discord_payload['id']}@discord.local",
        avatar=discord_payload.get("avatar") or "",
        hashed_token=hashlib.sha256(access_token.encode()).hexdigest())

    upsert_discord(db, user_data)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(url=f"{frontend_url}/?discord=connected", status_code=status.HTTP_302_FOUND)