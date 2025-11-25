from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter(prefix="/leagues", tags=["leagues"])

LEAGUES_DIR = Path("data/leagues")
LEAGUES_DIR.mkdir(parents=True, exist_ok=True)

class LeagueCreate(BaseModel):
    name: str

@router.post("/create")
def create_league(payload: LeagueCreate):
    league_name = payload.name.strip().lower().replace(" ", "-")

    league_path = LEAGUES_DIR / league_name

    if league_path.exists():
        raise HTTPException(status_code=400, detail="Liga já existe")

    try:
        league_path.mkdir(parents=True, exist_ok=True)
        return {"message": "Liga criada com sucesso", "league_id": league_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
