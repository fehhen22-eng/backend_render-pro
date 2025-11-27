import sys
from pathlib import Path

# --- Corrige caminho para reconhecer o diretório raiz ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

# ROTAS
from app.routes import leagues, teams, h2h
from app.routes.create_league import router as create_league_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas da API
app.include_router(leagues.router, prefix=settings.API_PREFIX)
app.include_router(teams.router, prefix=settings.API_PREFIX)
app.include_router(h2h.router, prefix=settings.API_PREFIX)
app.include_router(create_league_router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {
        "message": "H2H Predictor API",
        "version": settings.VERSION
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
