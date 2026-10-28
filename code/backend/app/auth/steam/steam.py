import os
import httpx
from urllib.parse import urlencode
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.auth.auth import create_oauth_state_token, decode_access_token, decode_oauth_state_token
from app.database import get_db
from app.steam.schema import SteamCreate
from app.steam.service import upsert_steam

load_dotenv()

router = APIRouter(prefix="/auth/steam", tags=["steam"])

@router.get("")
def steam_status():
    """
        Define -
        Entry -
        Exit -
    """
    return {"service": "steam", "status": "implemented"}

def link_creator(state):
    backend_url = os.getenv("BACKEND_URL")
    params = {
        "openid.return_to": f"{backend_url}/auth/steam/callback?state={state}",
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.realm": backend_url,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    return "https://steamcommunity.com/openid/login?" + urlencode(params)

def save_id():
    print("ID saved")

def save_infos(db, user_id, steam_id):
    upsert_steam(db, SteamCreate(user_id=int(user_id), steam_id=int(steam_id)))

def create_token(jwt):
    user_id = decode_access_token(jwt)["sub"]
    return create_oauth_state_token(user_id)


def create_callback():
    print("callback")

@router.get("/login")
def steam_login(jwt: str):
    token = create_token(jwt)
    link = link_creator(token)
    return RedirectResponse(link)
    # ① décoder le JWT → user_id
    # ② créer le state
    # ③ link = link_creator(state)
    # ④ rediriger vers link

def recover_id(request):
    claimed_id = request.query_params["openid.claimed_id"]
    return claimed_id.split("/")[-1]

def recover_user_id(request):
    state = request.query_params["state"]
    return decode_oauth_state_token(state)["sub"]

def is_steam_response_valid(request):
    params = dict(request.query_params)
    params["openid.mode"] = "check_authentication"
    response = httpx.post("https://steamcommunity.com/openid/login", data=params)
    return "is_valid:true" in response.text

def redirect_dashboard():
    frontend_url = os.getenv("FRONTEND_URL")
    return RedirectResponse(f"{frontend_url}/?steam=connected")


def get_player_infos(steam_id):
    params = {"key": os.getenv("STEAM_API_KEY"), "steamids": steam_id}
    response = httpx.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params=params)
    return response.json()["response"]["players"][0]

def get_player_lastgame(steam_id, count):
    params = {"key": os.getenv("STEAM_API_KEY"), "steamid": steam_id, "count": count}
    response = httpx.get("https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/", params=params)
    return response.json()["response"].get("games", [])


@router.get("/callback")
def steam_callback(request: Request, db: Session = Depends(get_db)):
    if not is_steam_response_valid(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Steam authentication failed.")
    steam_id = recover_id(request)
    if not steam_id.isdecimal():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Steam account ID.")
    user_id = recover_user_id(request)
    save_infos(db, user_id, steam_id)
    return redirect_dashboard()
    # ⑤ vérifier auprès de Steam
    # ⑥ lire l'ID
    # ⑦ save_infos(...)
    # ⑧ rediriger vers le dashboard


# 0) On récupère le jwt
# 1) Fabriquer un lien (jwt + callback)
# 2) On passe le lien au front
# 3) Une fois connecté, on sauvegarde les données.
# 4)