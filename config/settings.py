from pathlib import Path


class Settings:
    # Configurações do projeto
    PROJECT_NAME = "H2H Predictor API"
    VERSION = "1.0.0"
    API_PREFIX = "/api"
    
    # Configurações de CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5173",
        "https://*replit.dev",
        "https://*replit.app",
    ]
    
    # Configurações de dados
    DATA_DIR = Path(__file__).parent.parent / "data"
    LEAGUES_DIR = DATA_DIR / "leagues"
    
    # Configurações de atualização
    UPDATE_INTERVAL_HOURS = 48
    
    # Configurações do Sofascore
    SOFASCORE_BASE_URL = "https://www.sofascore.com"
    SOFASCORE_API_URL = "https://api.sofascore.com/api/v1"
    
    # Headers para requisições
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


settings = Settings()
