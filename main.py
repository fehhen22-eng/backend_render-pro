from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import csv

app = FastAPI()

# Permitir Base44 acessar o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "data/leagues"


# ----------------------------------------------------
# 🔍 FUNÇÕES AUXILIARES
# ----------------------------------------------------
def get_league_path(league_slug: str):
    return os.path.join(BASE_DIR, league_slug)


def get_team_csv_path(league_slug: str, team_slug: str):
    return os.path.join(BASE_DIR, league_slug, f"{team_slug}.csv")


def load_team_csv(league_slug: str, team_slug: str):
    path = get_team_csv_path(league_slug, team_slug)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="CSV do time não encontrado.")

    data = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            data.append(row)

    return data


# ----------------------------------------------------
# 📌 LISTAR LIGAS
# ----------------------------------------------------
@app.get("/api/leagues")
def list_leagues():
    if not os.path.exists(BASE_DIR):
        raise HTTPException(status_code=404, detail="Diretório 'leagues' não encontrado.")

    leagues = [
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ]

    return {"leagues": leagues}


# ----------------------------------------------------
# 📌 LISTAR TIMES DE UMA LIGA (FORMATO BASE44)
# ----------------------------------------------------
@app.get("/api/teams/{league_slug}")
def list_teams(league_slug: str):
    league_path = get_league_path(league_slug)

    if not os.path.exists(league_path):
        raise HTTPException(status_code=404, detail="Liga não encontrada.")

    teams = []
    for file in os.listdir(league_path):
        if file.endswith(".csv"):
            team_slug = file.replace(".csv", "")
            teams.append({
                "team_slug": team_slug,
                "team_name": team_slug.replace("-", " ").title()
            })

    return {"teams": teams}  # 🔥 Agora no formato que o Base44 exige


# ----------------------------------------------------
# 📌 H2H ENTRE DOIS TIMES (FORMATO BASE44)
# ----------------------------------------------------
@app.get("/api/h2h")
def h2h(league: str, home: str, away: str):
    league_slug = league
    home_slug = home
    away_slug = away

    # Carregar CSV dos times
    home_stats = load_team_csv(league_slug, home_slug)
    away_stats = load_team_csv(league_slug, away_slug)

    # Previsão extremamente simples (placeholder)
    prediction = {
        "better_team": home_slug if len(home_stats) >= len(away_stats) else away_slug,
        "confidence": 0.70,
    }

    # 🔥 FORMATO FINAL compatível com Base44
    return {
        "data": {
            "league": league_slug,
            "home": {
                "slug": home_slug,
                "name": home_slug.replace("-", " ").title(),
                "stats": home_stats
            },
            "away": {
                "slug": away_slug,
                "name": away_slug.replace("-", " ").title(),
                "stats": away_stats
            },
            "prediction": prediction
        }
    }


# ----------------------------------------------------
# ✔ TESTE RÁPIDO
# ----------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend H2H API rodando no Render 🔥"}
