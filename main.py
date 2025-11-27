# main.py
# Backend FastAPI único (colar inteiro como um arquivo main.py)
# Requer: fastapi, uvicorn, pandas, python-multipart (opcional)
# Ex.: requirements.txt -> fastapi, uvicorn[standard], pandas, python-multipart

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------- Config ----------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leagues"  # Espera: data/leagues/{league_slug}/{team_slug}.csv
DEFAULT_RECENT = 8  # quantos jogos usar por padrão nas métricas

# ---------- Utilitários ----------
def slugify(text: str) -> str:
    """Normaliza texto para slug (minusculas, sem acentos, '-' no lugar de espaço)."""
    if not isinstance(text, str):
        return ""
    # remove acentos
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text

def find_leagues() -> List[Dict[str, str]]:
    """Lista ligas encontradas em data/leagues como pastas ou CSVs."""
    if not DATA_DIR.exists():
        return []
    leagues = []
    # pastas (preferível)
    for p in sorted(DATA_DIR.iterdir()):
        if p.is_dir():
            leagues.append({"league_slug": p.name, "name": p.name})
    # Também procurar CSVs soltos (caso não use pastas)
    for csv in sorted(DATA_DIR.glob("*.csv")):
        slug = slugify(csv.stem)
        if not any(l["league_slug"] == slug for l in leagues):
            leagues.append({"league_slug": slug, "name": csv.stem})
    return leagues

def list_teams_in_league(league_slug: str) -> List[Dict[str, str]]:
    """Lista arquivos CSV (times) dentro de uma liga (pasta)."""
    target = DATA_DIR / league_slug
    teams = []
    if target.exists() and target.is_dir():
        for f in sorted(target.glob("*.csv")):
            team = f.stem
            teams.append({"team_slug": slugify(team), "team_name": team, "filename": f.name})
    else:
        # procura csv solto com prefix league_slug_
        for f in sorted(DATA_DIR.glob(f"{league_slug}_*.csv")):
            team = f.stem.replace(f"{league_slug}_", "")
            teams.append({"team_slug": slugify(team), "team_name": team, "filename": f.name})
    return teams

def load_team_csv(league_slug: str, team_slug: str) -> pd.DataFrame:
    """
    Tenta localizar e carregar o CSV do time.
    Procura:
      1) data/leagues/{league_slug}/{team_slug}.csv
      2) data/leagues/{league_slug}/{<original filename matching slug>.csv}
      3) data/leagues/{league_slug}_{team_slug}.csv
    """
    # 1: caminho direto
    d1 = DATA_DIR / league_slug / f"{team_slug}.csv"
    if d1.exists():
        return pd.read_csv(d1, sep=None, engine="python")
    # 2: buscar arquivo cujo slug equivale
    folder = DATA_DIR / league_slug
    if folder.exists() and folder.is_dir():
        for f in folder.glob("*.csv"):
            if slugify(f.stem) == team_slug:
                return pd.read_csv(f, sep=None, engine="python")
    # 3: arquivo no nível de leagues com prefix
    d3 = DATA_DIR / f"{league_slug}_{team_slug}.csv"
    if d3.exists():
        return pd.read_csv(d3, sep=None, engine="python")
    raise FileNotFoundError(f"CSV not found for team '{team_slug}' in league '{league_slug}'")

def recent_stats_from_df(df: pd.DataFrame, n: int = DEFAULT_RECENT) -> Dict[str, Any]:
    """
    Gera estatísticas simples a partir do CSV do time.
    Espera colunas que podem existir (tenta ser resiliente): 'GF', 'GA', 'FTHG', 'FTAG', 'GoalsFor', 'GoalsAgainst', 'HT', 'FT'
    Se o CSV for o modelo Angers (padrão do usuário), ele terá colunas de gols em HT/FT — tentamos inferir.
    """
    res = {"n_rows": len(df)}
    if df.empty:
        return res

    recent = df.tail(n).copy()
    # procurar colunas comuns
    cols = [c.lower() for c in recent.columns]
    # Tentativas: full-time goals colunas
    gf_col = None
    ga_col = None
    for cand in ["fthg", "goalsfor", "gf", "ft_goals_for", "goals_for"]:
        if cand in cols:
            gf_col = recent.columns[cols.index(cand)]
            break
    for cand in ["ftag", "goalsagainst", "ga", "ft_goals_against", "goals_against"]:
        if cand in cols:
            ga_col = recent.columns[cols.index(cand)]
            break
    # Se não encontrar, tentar interpretar por padrão (colunas numéricas de gols)
    if gf_col is None or ga_col is None:
        # heurística: procurar duas colunas numéricas consistentes
        numeric = [c for c in recent.columns if pd.api.types.is_numeric_dtype(recent[c])]
        if len(numeric) >= 2:
            gf_col = numeric[0] if gf_col is None else gf_col
            ga_col = numeric[1] if ga_col is None else ga_col

    # calcular somas e médias se possível
    try:
        if gf_col and ga_col:
            goals_for = recent[gf_col].astype(float)
            goals_against = recent[ga_col].astype(float)
            res.update({
                "gf_total": float(goals_for.sum()),
                "ga_total": float(goals_against.sum()),
                "gf_avg": float(goals_for.mean()),
                "ga_avg": float(goals_against.mean()),
                "over_1_5_pct": float((goals_for + goals_against > 1.5).sum() / len(recent) * 100),
                "over_2_5_pct": float((goals_for + goals_against > 2.5).sum() / len(recent) * 100),
                "btts_pct": float(((goals_for > 0) & (goals_against > 0)).sum() / len(recent) * 100),
            })
    except Exception:
        # se qualquer erro, apenas devolve contagem
        res["note"] = "Could not compute detailed stats from CSV columns"
    return res

def make_prediction(home_stats: Dict[str, Any], away_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera uma previsão simples baseada em médias de gols e diferença.
    Regras simples:
      - calcula expected_home = home.gf_avg * 0.6 + away.ga_avg * 0.4 (heurística)
      - se diff >= 0.35 -> favorito
      - indica tendência Over/Under com base em medias combinadas
    """
    hg = home_stats.get("gf_avg") or 0.0
    ag = away_stats.get("ga_avg") or 0.0
    eg_home = hg * 0.6 + ag * 0.4

    ag_home = home_stats.get("ga_avg") or 0.0
    ag_away = away_stats.get("gf_avg") or 0.0
    eg_away = ag_away * 0.6 + ag_home * 0.4

    diff = eg_home - eg_away
    winner = "draw"
    if diff >= 0.35:
        winner = "home"
    elif diff <= -0.35:
        winner = "away"

    combined_over_2_5 = None
    try:
        combined_over_2_5 = round((home_stats.get("over_2_5_pct", 0) + away_stats.get("over_2_5_pct", 0)) / 2, 2)
    except Exception:
        combined_over_2_5 = None

    return {
        "expected_goals_home": round(eg_home, 2),
        "expected_goals_away": round(eg_away, 2),
        "difference": round(diff, 2),
        "suggested_winner": winner,
        "combined_over_2_5_pct": combined_over_2_5,
    }

# ---------- FastAPI app ----------
app = FastAPI(title="H2H Predictor - Simple Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class LeagueOut(BaseModel):
    league_slug: str
    name: str

class TeamOut(BaseModel):
    team_slug: str
    team_name: str
    filename: str

class H2HQuery(BaseModel):
    league: str
    home: str
    away: str
    recent: Optional[int] = DEFAULT_RECENT

# ---------- Routes ----------
@app.get("/api/leagues", response_model=List[LeagueOut])
def api_list_leagues():
    """Lista ligas encontradas no diretório data/leagues."""
    leagues = find_leagues()
    return leagues

@app.get("/api/teams/{league_slug}", response_model=List[TeamOut])
def api_list_teams(league_slug: str):
    """Lista times disponíveis dentro de uma liga (slug)."""
    teams = list_teams_in_league(league_slug)
    if not teams:
        raise HTTPException(status_code=404, detail=f"No teams found for league '{league_slug}'")
    return teams

@app.get("/api/h2h")
def api_h2h(league: str = Query(...), home: str = Query(...), away: str = Query(...), recent: int = Query(DEFAULT_RECENT)):
    """
    Análise H2H mínima:
    - Carrega os CSVs dos dois times
    - Calcula estatísticas recentes
    - Retorna ambos os resumos e uma sugestão simples
    """
    league_slug = slugify(league)
    home_slug = slugify(home)
    away_slug = slugify(away)

    # load CSVs
    try:
        df_home = load_team_csv(league_slug, home_slug)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        df_away = load_team_csv(league_slug, away_slug)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # basic stats
    home_stats = recent_stats_from_df(df_home, n=recent)
    away_stats = recent_stats_from_df(df_away, n=recent)

    # prediction
    prediction = make_prediction(home_stats, away_stats)

    return {
        "league": league_slug,
        "home": {"slug": home_slug, "name": home, "stats": home_stats},
        "away": {"slug": away_slug, "name": away, "stats": away_stats},
        "prediction": prediction,
    }

@app.get("/api/raw/{league_slug}/{team_slug}")
def api_raw_csv(league_slug: str, team_slug: str):
    """Retorna as primeiras linhas do CSV do time para debug (JSON)."""
    try:
        df = load_team_csv(league_slug, team_slug)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # limitar saída para evitar payload gigante
    preview = df.head(50).to_dict(orient="records")
    return {"rows": preview, "columns": list(df.columns)}

# ---------- Health / debug ----------
@app.get("/api/health")
def health():
    return {"status": "ok", "data_dir_exists": DATA_DIR.exists()}

# if running with `python main.py` (not necessary on Render)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False, log_level="info")
