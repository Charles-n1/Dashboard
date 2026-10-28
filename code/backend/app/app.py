"""
    app.py
    This file contains the core of the FastAPI app
"""

#region Imports

import os
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from app.auth.auth import router as auth_router
from app.auth.discord.discord import router as auth_discord_router
from app.auth.steam.steam import router as auth_steam_router
from app.auth.weather.weather import router as auth_weather_router

from app.user.route import router as user_router
from app.discord.route import router as discord_router
from app.steam.route import router as steam_router
from app.weather.route import router as weather_router
from app.grid.route import router as grid_router
from app.cell.route import router as cell_router

from app.utils.page_structure import (
    ROOT_PAGE,
    EXCEPTION_404_PAGE,
    EXCEPTION_500_PAGE
)

from app.utils.constants import (
    WUNDERBAR_DASHBOARD_API_TITLE,
    WUNDERBAR_DASHBOARD_API_DESCRIPTION,
    WIDGET_CATALOG,
)

#endregion

#region FastAPI App Initialization

app = FastAPI(title=WUNDERBAR_DASHBOARD_API_TITLE, description=WUNDERBAR_DASHBOARD_API_DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(auth_steam_router)
app.include_router(auth_router)
app.include_router(auth_discord_router)
app.include_router(auth_steam_router)
app.include_router(auth_weather_router)
app.include_router(discord_router)
app.include_router(steam_router)
app.include_router(weather_router)
app.include_router(grid_router)
app.include_router(cell_router)
app.include_router(user_router)

#endregion

#region Routes and Exception Handlers

@app.get("/", response_class=HTMLResponse)
def root():
    """
        Define -
        Entry -
        Exit -
    """
    return ROOT_PAGE


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    """
        Define -
        Entry -
        Exit -
    """
    favicon_path = ""
    if favicon_path.is_file():
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404)


@app.get("/about.json")
def about(request: Request):
    """
        Define -
        Entry -
        Exit -
    """
    return {
        "client": {"host": request.client.host if request.client else "unknown"},
        "server":
        {
            "current_time": int(time.time()),
            "services": WIDGET_CATALOG, # TODO Automated widget getter in python 
        },
    }


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
        Define -
        Entry -
        Exit -
    """
    if exc.status_code == 404:
        return HTMLResponse(
            content=EXCEPTION_404_PAGE,
            status_code=404,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def custom_generic_exception_handler(request: Request, exc: Exception):
    """
        Define -
        Entry -
        Exit -
    """
    return HTMLResponse(
        content=EXCEPTION_500_PAGE,
        status_code=500,
    )

#endregion