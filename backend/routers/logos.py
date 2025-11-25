from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..utils.logo_cache import get_or_download_logo, cache_exists
from pathlib import Path

router = APIRouter()


@router.get("/logos/{team_id}")
async def get_team_logo(team_id: int):
    """
    Retorna o logo de uma equipe.
    Se o logo não estiver em cache, será baixado da API SofaScore.
    """
    logo_path = get_or_download_logo(team_id)
    
    if logo_path and Path(logo_path).exists():
        return FileResponse(
            logo_path,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=31536000",  # Cache por 1 ano
            }
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Logo não encontrado para a equipe com ID {team_id}"
        )


@router.get("/logos/{team_id}/exists")
async def check_logo_cache(team_id: int):
    """
    Verifica se o logo de uma equipe está em cache.
    """
    exists = cache_exists(team_id)
    return {"team_id": team_id, "cached": exists}
