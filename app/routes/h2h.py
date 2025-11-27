from fastapi import APIRouter, HTTPException, Body
from typing import Dict
from pydantic import BaseModel

from app.services.h2h_analyzer import h2h_analyzer
from app.services.update_csv import update_service



router = APIRouter(prefix="/h2h", tags=["h2h"])


class H2HRequest(BaseModel):
    """Modelo de requisição para análise H2H."""
    league_id: str
    team1_id: str
    team2_id: str


class UpdateRequest(BaseModel):
    """Modelo de requisição para atualização de dados."""
    league_id: str
    team_id: str


@router.post("", response_model=Dict)
async def analyze_h2h(
    request: H2HRequest = Body(...)
):
    """
    Analisa o confronto entre dois times.
    """
    try:
        analysis = h2h_analyzer.analyze_h2h(
            request.league_id,
            request.team1_id,
            request.team2_id
        )
        
        if "error" in analysis:
            raise HTTPException(status_code=404, detail=analysis["error"])
        
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao analisar confronto: {str(e)}")


@router.post("/update/team")
async def update_team_data(
    request: UpdateRequest = Body(...)
):
    """
    Atualiza os dados de um time específico do Sofascore.
    """
    try:
        success = await update_service.update_team(
            request.league_id,
            request.team_id
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Dados do time {request.team_id} atualizados com sucesso"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Falha ao atualizar dados do time"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar dados: {str(e)}")


@router.post("/update/league/{league_id}")
async def update_league_data(league_id: str):
    """
    Atualiza os dados de todos os times de uma liga.
    """
    try:
        result = await update_service.update_league(league_id)
        return {
            "status": "success",
            "league": league_id,
            "updated": result["updated"],
            "failed": result["failed"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar liga: {str(e)}")


@router.post("/update/all")
async def update_all_data():
    """
    Atualiza os dados de todos os times de todas as ligas.
    """
    try:
        result = await update_service.update_all_teams()
        return {
            "status": "success",
            "updated": result["updated"],
            "failed": result["failed"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar todos os dados: {str(e)}")
