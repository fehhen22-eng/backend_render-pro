from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from ..utils.h2h_engine import analyze_h2h, analyze_asian_markets

router = APIRouter(tags=["H2H"])
BASE = Path("data/leagues")


@router.get("/h2h")
def h2h(league: str, home: str, away: str):
    """
    Lê os CSVs do mandante e visitante e retorna a análise H2H
    usando o motor definido em utils.h2h_engine.analyze_h2h.
    """
    league_path = BASE / league
    home_csv = league_path / f"{home}.csv"
    away_csv = league_path / f"{away}.csv"

    if not home_csv.exists() or not away_csv.exists():
        raise HTTPException(status_code=404, detail="CSV de time não encontrado para a liga informada.")

    df_home = pd.read_csv(home_csv, sep=";")
    df_away = pd.read_csv(away_csv, sep=";")

    result = analyze_h2h(df_home, df_away)
    
    # Analisa mercados asiáticos
    asian_markets = analyze_asian_markets(df_home, df_away, home, away)
    
    return {
        "league": league,
        "home": home,
        "away": away,
        "analysis": result,
        "asian_markets": asian_markets,
    }
