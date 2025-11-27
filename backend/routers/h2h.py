from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.utils.file_manager import list_teams
from services.h2h_analyzer import build_h2h_response
from utils.team_normalizer import slugify

router = APIRouter(prefix="/h2h", tags=["H2H"])

# Caminho REAL da pasta de CSVs
BASE = Path(__file__).resolve().parent.parent.parent / "data" / "leagues"


@router.get("")
def h2h(league: str, home: str, away: str):
    """
    Analisa confronto H2H com base nos CSVs de cada time
    e retorna:
    - resumo home
    - resumo away
    - favorito
    - confiança
    - tendência gols
    - tendência escanteios
    - dica principal
    - mercados asiáticos
    """

    league_path = BASE / league

    if not league_path.exists():
        raise HTTPException(status_code=404, detail=f"Liga '{league}' não encontrada.")

    # Normaliza nomes dos arquivos (Barcelona → barcelona.csv)
    home_slug = slugify(home)
    away_slug = slugify(away)

    home_csv = league_path / f"{home_slug}.csv"
    away_csv = league_path / f"{away_slug}.csv"

    if not home_csv.exists():
        raise HTTPException(status_code=404, detail=f"Time '{home}' não encontrado na liga '{league}'.")

    if not away_csv.exists():
        raise HTTPException(status_code=404, detail=f"Time '{away}' não encontrado na liga '{league}'.")

    # Suporte para ; ou ,
    df_home = pd.read_csv(home_csv, sep=";|,", engine="python")
    df_away = pd.read_csv(away_csv, sep=";|,", engine="python")

    # Usa o motor H2H PROFISSIONAL
    response = build_h2h_response(
        league_id=league,
        home_df=df_home,
        away_df=df_away,
        home_name=home,
        away_name=away
    )

    return response
