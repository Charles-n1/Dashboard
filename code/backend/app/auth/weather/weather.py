from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth/weather", tags=["weather"])

@router.get("")
def weather_status():
    """
        Define -
        Entry -
        Exit -
    """
    return {"service": "weather", "status": "implemented"}
