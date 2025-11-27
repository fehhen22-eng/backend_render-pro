import os
from pathlib import Path
from typing import List, Optional
import pandas as pd
from app.utils.team_normalizer import slugify


def get_data_path() -> Path:
    """Retorna o caminho base do diretório data."""
    return Path(__file__).resolve().parent.parent.parent / "data"


def get_leagues_path() -> Path:
    """Retorna o caminho do diretório leagues."""
    return get_data_path() / "leagues"


def list_leagues() -> List[dict]:
    """Lista todas as ligas disponíveis."""
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
    """Lista todos os times de uma liga específica."""
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
    """Carrega dados de um time em CSV."""
    csv_path = get_leagues_path() / league_id / f"{team_id}.csv"

    if not csv_path.exists():
        return None

    try:
        df = pd.read_csv(csv_path, sep=";|,", engine="python")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do time {team_id}: {e}")
        return None


def save_team_csv(league_id: str, filename: str, file_bytes: bytes) -> str:
    """Salva um arquivo CSV enviado via upload."""
    league_path = get_leagues_path() / league_id
    league_path.mkdir(parents=True, exist_ok=True)

    cleaned = slugify(filename.replace(".csv", "")) + ".csv"
    dest = league_path / cleaned

    try:
        with open(dest, "wb") as f:
            f.write(file_bytes)
        return cleaned
    except Exception as e:
        print(f"Erro ao salvar CSV {cleaned}: {e}")
        raise e


def save_team_data(league_id: str, team_id: str, df: pd.DataFrame) -> bool:
    """Salva DataFrame vindo do SofaScore."""
    league_path = get_leagues_path() / league_id
    league_path.mkdir(parents=True, exist_ok=True)

    csv_path = league_path / f"{team_id}.csv"

    try:
        df.to_csv(csv_path, index=False, sep=";")
        return True
    except Exception as e:
        print(f"Erro ao salvar dados do time {team_id}: {e}")
        return False
