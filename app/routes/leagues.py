from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.utils.file_manager import list_leagues

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("", response_model=List[Dict])
async def get_leagues():
    """
    Lista todas as ligas disponíveis.
    """
    try:
        leagues = list_leagues()
        return leagues
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ligas: {str(e)}")
