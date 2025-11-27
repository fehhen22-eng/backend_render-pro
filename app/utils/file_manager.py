import os
from pathlib import Path
import pandas as pd
from typing import List, Optional
from app.utils.team_normalizer import slugify


def get_data_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "data"


def get_leagues_path() -> Path:
    return get_data_path() / "leagues"


def list_leagues() -> List[dict]:
    leagues_path = get_leagues_path()
    if not leagues_path.exists():
        return []

    leagues = []
    for item in sorted(leagues_path.iterdir()):
        if item.is_dir():
            league_id = item.name
            leagues.append({
                "league_id": league_id,
                "name": league_id.replace("-", " ").title()
            })
    return leagues


def list_teams(league_id: str) -> List[dict]:
    league_path = get_leagues_path() / league_id
    if not league_path.exists():
        return []

    teams = []
    for csv_file in sorted(league_path.glob("*.csv")):
        team_id = csv_file.stem
        teams.append({
            "team_id": team_id,
            "name": team_id.replace("-", " ").title()
        })
    return teams


def load_team_data(league_id: str, team_id: str) -> Optional[pd.DataFrame]:
    csv_path = get_leagues_path() / league_id / f"{team_id}.csv"

    if not csv_path.exists():
        return None

    try:
        df = pd.read_csv(csv_path, sep=";|,", engine="python")
        return df
    except Exception:
        return None
