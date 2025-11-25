from fastapi import APIRouter
from pathlib import Path
from typing import Optional
import json

router = APIRouter(tags=["Leagues"])

BASE = Path("data/leagues")


@router.get("/leagues")
def list_leagues():
    """
    Lista todas as ligas presentes em data/leagues,
    lendo opcionalmente o arquivo liga.json de cada pasta.
    """
    leagues = []

    if not BASE.exists():
        return {"leagues": []}

    for liga in BASE.iterdir():
        if not liga.is_dir():
            continue

        info = {
            "league_id": liga.name,
            "name": liga.name,
        }

        meta_file = liga / "liga.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # mescla dados do JSON, sem sobrescrever o league_id
                for k, v in data.items():
                    if k == "league":
                        info.setdefault("name", v)
                    else:
                        info[k] = v
            except Exception:
                # se der erro de leitura, ignora o JSON e segue
                pass

        leagues.append(info)

    leagues.sort(key=lambda x: x.get("name", "").lower())
    return {"leagues": leagues}


@router.post("/create-league")
def create_league(
    league_name: str,
    league_id: Optional[str] = None,
    season_id: Optional[str] = None,
    country: Optional[str] = None
):
    """
    Cria uma nova liga em data/leagues/{slug}/ com um liga.json completo.
    """
    league_slug = league_name.strip().lower().replace(" ", "-")
    league_path = BASE / league_slug
    league_path.mkdir(parents=True, exist_ok=True)

    liga_json = league_path / "liga.json"
    
    # Prepara os dados completos da liga
    liga_data = {
        "league": league_name.strip(),
        "league_slug": league_slug
    }
    
    if league_id:
        liga_data["league_id"] = league_id
    if season_id:
        liga_data["season_id"] = season_id
    if country:
        liga_data["country"] = country
    
    # Cria ou atualiza o arquivo liga.json
    with open(liga_json, "w", encoding="utf-8") as f:
        json.dump(liga_data, f, ensure_ascii=False, indent=2)

    return {"status": "ok", "league": league_slug, "data": liga_data}
