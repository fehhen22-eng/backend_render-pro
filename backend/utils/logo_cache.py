import os
import requests
from pathlib import Path
from typing import Optional

BASE = "https://api.sofascore.com/api/v1"
HDR = {"User-Agent": "Mozilla/5.0"}

LOGOS_DIR = Path(__file__).parent.parent / "data" / "team_logos"


def get_team_logo_path(team_id: int) -> Path:
    """Retorna o caminho do logo de uma equipe pelo ID."""
    return LOGOS_DIR / f"{team_id}.png"


def download_team_logo(team_id: int) -> Optional[str]:
    """
    Baixa o logo de uma equipe da API SofaScore e salva localmente.
    Retorna o caminho do arquivo se bem-sucedido, None caso contrário.
    """
    logo_path = get_team_logo_path(team_id)
    
    # Se já existe, retorna o caminho
    if logo_path.exists():
        return str(logo_path)
    
    # Garante que o diretório existe
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # URL do logo da equipe
        logo_url = f"{BASE}/team/{team_id}/image"
        
        # Baixa o logo
        response = requests.get(logo_url, headers=HDR, timeout=10)
        
        if response.status_code == 200:
            # Salva o arquivo
            with open(logo_path, "wb") as f:
                f.write(response.content)
            return str(logo_path)
        else:
            print(f"Falha ao baixar logo para team_id {team_id}: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erro ao baixar logo para team_id {team_id}: {e}")
        return None


def get_or_download_logo(team_id: int) -> Optional[str]:
    """
    Retorna o caminho do logo de uma equipe.
    Se não existir localmente, tenta baixar da API.
    """
    logo_path = get_team_logo_path(team_id)
    
    if logo_path.exists():
        return str(logo_path)
    
    return download_team_logo(team_id)


def cache_exists(team_id: int) -> bool:
    """Verifica se o logo de uma equipe já está em cache."""
    return get_team_logo_path(team_id).exists()
