from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from app.routes import leagues, teams, h2h
from app.routes.create_league import router as create_league_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leagues.router, prefix=settings.API_PREFIX)
app.include_router(teams.router, prefix=settings.API_PREFIX)
app.include_router(h2h.router, prefix=settings.API_PREFIX)
app.include_router(create_league_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "H2H Predictor API",
        "version": settings.VERSION,
        "endpoints": {
            "leagues": f"{settings.API_PREFIX}/leagues",
            "teams": f"{settings.API_PREFIX}/teams/{{league_id}}",
            "h2h": f"{settings.API_PREFIX}/h2h"
        }
    }


@app.get("/health")
async def health():
    """Endpoint de health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )
