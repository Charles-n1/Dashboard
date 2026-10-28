import httpx
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import User
from app.dependencies import get_current_user
from app.weather.schema import WeatherQuery


router = APIRouter(prefix="/weather", tags=["weather"])

def _fetch_open_meteo(url: str, params: dict, what: str):
    try:
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve {what} from Open-Meteo.",
        ) from exc


@router.get("/forecast")
@router.get("")
def get_weather(query: Annotated[WeatherQuery, Query()]):
    return _fetch_open_meteo(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": query.latitude,
            "longitude": query.longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
        },
        "weather data",
    )


@router.get("/air-quality")
def get_air_quality(query: Annotated[WeatherQuery, Query()]):
    return _fetch_open_meteo(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        {
            "latitude": query.latitude,
            "longitude": query.longitude,
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,european_aqi",
        },
        "air quality data",
    )