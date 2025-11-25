from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import shutil

router = APIRouter(tags=["Upload CSV"])
BASE = Path("data/leagues")


@router.post("/upload-csv")
async def upload_csv(
    league: str = Form(...),
    team_name: str = Form(...),
    file: UploadFile = File(...)
):
    league_path = BASE / league
    league_path.mkdir(parents=True, exist_ok=True)

    filename = f"{team_name.lower().replace(' ', '-').strip()}.csv"
    dest = league_path / filename

    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "ok",
        "msg": "CSV salvo com sucesso",
        "path": str(dest)
    }
