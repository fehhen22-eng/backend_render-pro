from pathlib import Path


class Settings:
    # ===========================
    # CONFIGURAÇÕES DO PROJETO
    # ===========================
    PROJECT_NAME = "H2H Predictor API"
    VERSION = "1.0.0"
    API_PREFIX = "/api"

    # ===========================
    # DIRETÓRIOS GLOBAIS
    # ===========================
    # raiz do projeto (onde ficam /app e /data)
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    # /data
    DATA_DIR = PROJECT_ROOT / "data"

    # /data/leagues
    LEAGUES_DIR = DATA_DIR / "leagues"


    # ===========================
    # CONFIGS CORS
    # ===========================
    CORS_ORIGINS = ["*"]


    # ===========================
    # ATUALIZAÇÃO DOS CSVs
    # ===========================
    UPDATE_INTERVAL_HOURS = 48


    # ===========================
    # CONFIGURAÇÕES SOFASCORE
    # ===========================
    SOFASCORE_BASE_URL = "https://www.sofascore.com"
    SOFASCORE_API_URL = "https://api.sofascore.com/api/v1"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }


settings = Settings()
