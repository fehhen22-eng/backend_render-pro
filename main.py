from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORTAÇÕES CERTAS
from app.routes.h2h import router as h2h_router
from app.routes.leagues import router as leagues_router
from app.routes.teams import router as teams_router

app = FastAPI(
    title="H2H Predictor Backend",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTAS
app.include_router(h2h_router, prefix="/h2h")
app.include_router(leagues_router, prefix="/leagues")
app.include_router(teams_router, prefix="/teams")


@app.get("/")
def root():
    return {"message": "Backend H2H Predictor ONLINE"}
