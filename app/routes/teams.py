from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict
from app.utils.file_manager import list_teams


router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/{league_id}", response_model=List[Dict])
async def get_teams(
    league_id: str = Path(..., description="ID da liga")
):
    """
    Lista todos os times de uma liga específica.
    
    Args:
        league_id: ID da liga (ex: 'laliga', 'premier-league')
    
    Returns:
        Lista de times com id e nome.
    """
    try:
        teams = list_teams(league_id)
        
        if not teams:
            raise HTTPException(
                status_code=404,
                detail=f"Liga '{league_id}' não encontrada ou sem times cadastrados"
            )
        
        return teams
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar times: {str(e)}")
