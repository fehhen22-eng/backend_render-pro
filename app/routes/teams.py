from fastapi import APIRouter, HTTPException, Path, UploadFile, File
from typing import List, Dict
from app.utils.file_manager import list_teams, save_team_csv

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/{league_id}", response_model=List[Dict])
async def get_teams(
    league_id: str = Path(..., description="ID da liga")
):
    """
    Lista todos os times de uma liga específica.
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


@router.post("/{league_id}/upload")
async def upload_team_csv(
    league_id: str = Path(..., description="ID da liga"),
    file: UploadFile = File(...)
):
    """
    Upload de arquivo CSV de um time específico.
    Salva em: data/leagues/{league_id}/{team}.csv
    """
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Envie apenas arquivos .csv")

        file_bytes = await file.read()

        saved_filename = save_team_csv(
            league_id=league_id,
            filename=file.filename,
            file_bytes=file_bytes
        )

        return {
            "message": "Time salvo com sucesso",
            "filename": saved_filename,
            "league_id": league_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar time: {str(e)}")
