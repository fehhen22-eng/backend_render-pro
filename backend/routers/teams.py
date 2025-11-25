from fastapi import APIRouter
from pathlib import Path
import pandas as pd

router = APIRouter(tags=["Teams"])
BASE = Path("data/leagues")


@router.get("/league/{league_id}/teams")
def teams_of_league(league_id: str):
    """
    Retorna a lista de times de uma liga a partir dos arquivos CSV.
    Se o CSV tiver colunas team_name ou team_id, elas também são retornadas.
    """
    league_path = BASE / league_id
    if not league_path.exists():
        return {"league": league_id, "teams": []}

    teams = []
    for csv_file in league_path.glob("*.csv"):
        slug = csv_file.stem
        display_name = slug
        team_id = None

        try:
            df_head = pd.read_csv(csv_file, sep=";", nrows=1)
            if "team_name" in df_head.columns:
                display_name = str(df_head["team_name"].iloc[0])
            if "team_id" in df_head.columns:
                team_id = int(df_head["team_id"].iloc[0])
        except Exception:
            # se não conseguir ler o CSV, segue apenas com o slug
            pass

        teams.append({
            "team": slug,
            "display_name": display_name,
            "team_id": team_id,
            "filename": csv_file.name,
        })

    teams.sort(key=lambda t: (t["display_name"] or "").lower())
    return {"league": league_id, "teams": teams}
