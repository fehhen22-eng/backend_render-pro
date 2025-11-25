from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

import pandas as pd

from .sofascorer import (
    search_team_and_get_id,
    fetch_team_stats,
    fetch_table_position,
)

# Tenta importar APScheduler, mas não torna obrigatório
try:
    from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
except Exception:  # pragma: no cover
    BackgroundScheduler = None  # type: ignore


DATA_BASE = Path("data/leagues")
_scheduler = None  # instância global do scheduler (se usado)


def _ensure_basic_columns(df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
    """
    Garante que colunas básicas existam no DataFrame, sem remover nada.
    """
    for key, value in info.items():
        if key not in df.columns:
            df[key] = value
        else:
            # atualiza o valor da primeira linha; se quiser linha a linha, adapte
            df.loc[:, key] = value
    return df


def _update_team_dataframe(df: pd.DataFrame, team_slug: str) -> pd.DataFrame:
    """
    Recebe o DataFrame original do CSV e devolve o DataFrame atualizado,
    sem apagar colunas existentes. Apenas atualiza e adiciona colunas novas.
    """
    # 1) Garante que temos team_id e team_name
    team_id: Optional[int] = None
    team_name: Optional[str] = None

    if "team_id" in df.columns:
        try:
            team_id = int(df["team_id"].iloc[0])
        except Exception:
            team_id = None

    if "team_name" in df.columns:
        try:
            team_name = str(df["team_name"].iloc[0])
        except Exception:
            team_name = None

    if team_id is None or not team_name:
        info = search_team_and_get_id(team_slug)
        team_id = info["team_id"]
        team_name = info["team_name"]

    # 2) Busca estatísticas (SIMULADAS no momento)
    stats = fetch_team_stats(team_id)
    position = fetch_table_position(team_id)

    # 3) Monta dicionário de atualização
    update_info: Dict[str, Any] = {
        "team_id": team_id,
        "team_name": team_name,
        "table_position": position,
        "last_update_utc": datetime.utcnow().isoformat(),
    }
    update_info.update(stats)

    # 4) Aplica no DataFrame SEM apagar colunas antigas
    df = _ensure_basic_columns(df, update_info)
    return df


def update_team_csv(csv_path: Path) -> Dict[str, Any]:
    """
    Atualiza um único CSV de time.
    """
    if not csv_path.exists():
        return {"file": str(csv_path), "updated": False, "reason": "CSV não encontrado"}

    team_slug = csv_path.stem

    try:
        df = pd.read_csv(csv_path, sep=";")
    except Exception as exc:
        return {"file": str(csv_path), "updated": False, "reason": f"Erro ao ler CSV: {exc}"}

    df_updated = _update_team_dataframe(df, team_slug)

    try:
        df_updated.to_csv(csv_path, sep=";", index=False)
    except Exception as exc:
        return {"file": str(csv_path), "updated": False, "reason": f"Erro ao salvar CSV: {exc}"}

    return {"file": str(csv_path), "updated": True}


def update_league(league_id: str) -> Dict[str, Any]:
    """
    Atualiza todos os times de uma liga específica.
    """
    league_path = DATA_BASE / league_id
    if not league_path.exists():
        return {"league": league_id, "teams": []}

    results: List[Dict[str, Any]] = []
    for csv_file in league_path.glob("*.csv"):
        results.append(update_team_csv(csv_file))

    return {"league": league_id, "teams": results}


def update_all_leagues() -> List[Dict[str, Any]]:
    """
    Percorre todas as ligas em data/leagues e chama update_league para cada uma.
    """
    if not DATA_BASE.exists():
        return []

    output: List[Dict[str, Any]] = []
    for liga in DATA_BASE.iterdir():
        if liga.is_dir():
            output.append(update_league(liga.name))
    return output


def schedule_background_updates() -> None:
    """
    Agenda a atualização automática de todas as ligas a cada 48 horas,
    usando APScheduler, caso esteja instalado.

    Se não houver APScheduler, simplesmente não agenda nada.
    """
    global _scheduler, BackgroundScheduler

    if BackgroundScheduler is None:
        # APScheduler não está disponível; não faz nada
        return

    if _scheduler is not None:
        # Já inicializado
        return

    scheduler = BackgroundScheduler()
    # A cada 48 horas
    scheduler.add_job(update_all_leagues, "interval", hours=48, id="update_all_leagues", replace_existing=True)
    scheduler.start()
    _scheduler = scheduler
