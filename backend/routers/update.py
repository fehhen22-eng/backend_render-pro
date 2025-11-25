from fastapi import APIRouter, HTTPException
from ..updater.update_engine import update_all_leagues, update_league

router = APIRouter(tags=["Update"])


@router.get("/update/all")
def update_all():
    """
    Atualiza todas as ligas e times encontrados em data/leagues.
    """
    result = update_all_leagues()
    return {"status": "ok", "updated": result}


@router.get("/update/league/{league_id}")
def update_one(league_id: str):
    """
    Atualiza todos os times de uma liga específica.
    """
    result = update_league(league_id)
    if not result["teams"]:
        raise HTTPException(status_code=404, detail="Liga não encontrada ou sem CSVs.")
    return {"status": "ok", **result}
