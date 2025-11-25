from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.leagues import router as leagues_router
from .routers.teams import router as teams_router
from .routers.h2h import router as h2h_router
from .routers.upload import router as upload_router
from .routers.update import router as update_router
from .routers.logos import router as logos_router

from .updater.update_engine import schedule_background_updates

app = FastAPI(title="Base44 H2H Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(leagues_router, prefix="/api")
app.include_router(teams_router, prefix="/api")
app.include_router(h2h_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(update_router, prefix="/api")
app.include_router(logos_router, prefix="/api")

@app.on_event("startup")
def _start_scheduler() -> None:
    """
    Inicializa o scheduler em background para atualizar as ligas a cada 48 horas.
    Se o APScheduler não estiver instalado, a função simplesmente não faz nada,
    assim o backend continua funcionando normalmente.
    """
    schedule_background_updates()

@app.get("/")
def root():
    return {
        "status": "online",
        "backend": "Base44 H2H Backend v2",
        "message": "API H2H + updater incremental de CSVs ativa"
    }
