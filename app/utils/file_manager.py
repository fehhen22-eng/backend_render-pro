import os
from pathlib import Path
from typing import List, Optional
import pandas as pd


def get_data_path() -> Path:
    """Retorna o caminho base do diretório data."""
    return Path(__file__).parent.parent.parent / "data"


def get_leagues_path() -> Path:
    """Retorna o caminho do diretório leagues."""
    return get_data_path() / "leagues"


def list_leagues() -> List[dict]:
    """
    Lista todas as ligas disponíveis.
    Retorna uma lista de dicionários com id e name.
    """
    leagues_path = get_leagues_path()
    
    if not leagues_path.exists():
        return []
    
    leagues = []
    for item in sorted(leagues_path.iterdir()):
        if item.is_dir():
            league_id = item.name
            league_name = league_id.replace("-", " ").title()
            leagues.append({
                "id": league_id,
                "name": league_name
            })
    
    return leagues


def list_teams(league_id: str) -> List[dict]:
    """
    Lista todos os times de uma liga específica.
    Retorna uma lista de dicionários com id e name.
    """
    league_path = get_leagues_path() / league_id
    
    if not league_path.exists():
        return []
    
    teams = []
    for csv_file in sorted(league_path.glob("*.csv")):
        team_id = csv_file.stem
        team_name = team_id.replace("-", " ").title()
        teams.append({
            "id": team_id,
            "name": team_name
        })
    
    return teams


def load_team_data(league_id: str, team_id: str) -> Optional[pd.DataFrame]:
    """
    Carrega os dados de um time específico.
    Retorna um DataFrame ou None se o arquivo não existir.
    """
    csv_path = get_leagues_path() / league_id / f"{team_id}.csv"
    
    if not csv_path.exists():
        return None
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do time {team_id}: {e}")
        return None


def save_team_data(league_id: str, team_id: str, df: pd.DataFrame) -> bool:
    """
    Salva os dados de um time.
    Retorna True se salvou com sucesso, False caso contrário.
    """
    league_path = get_leagues_path() / league_id
    league_path.mkdir(parents=True, exist_ok=True)
    
    csv_path = league_path / f"{team_id}.csv"
    
    try:
        df.to_csv(csv_path, index=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados do time {team_id}: {e}")
        return False
        def save_team_data(league_id: str, team_id: str, df) -> bool:
    """
    Salva o DataFrame do Sofascore em CSV dentro de data/leagues/{league}/{team}.csv
    """
    league_path = LEAGUES_DIR / league_id
    league_path.mkdir(parents=True, exist_ok=True)

    filename = f"{team_id}.csv"
    filepath = league_path / filename

    try:
        df.to_csv(filepath, index=False, sep=";")
        return True
    except Exception as e:
        print(f"Erro ao salvar CSV de {team_id}: {e}")
        return False

