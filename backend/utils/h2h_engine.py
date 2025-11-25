from typing import Dict, Any, List

import pandas as pd


def _safe_mean(df: pd.DataFrame, columns, default: float) -> float:
    """
    Tenta vários nomes de coluna até encontrar um válido.
    Aceita string única ou lista de strings.
    """
    if isinstance(columns, str):
        columns = [columns]

    for col in columns:
        try:
            if col in df.columns:
                value = df[col].astype(float).mean()
                if not pd.isna(value):
                    return float(value)
        except Exception:
            continue
    return float(default)


def analyze_h2h(df_home: pd.DataFrame, df_away: pd.DataFrame) -> Dict[str, Any]:
    """
    Análise H2H RESUMIDA.
    O painel atual só usa `asian_markets`, então aqui mantemos algo simples,
    mas já coerente para futuras expansões.
    """

    home_win = _safe_mean(df_home, ["win_rate", "home_win_rate"], 50.0)
    away_win = _safe_mean(df_away, ["win_rate", "away_win_rate"], 50.0)

    # Probabilidade média de vitória de cada lado
    home_win = max(10.0, min(80.0, home_win))
    away_win = max(10.0, min(80.0, away_win))

    # Empate como peso residual, limitado para não ficar absurdo
    draw = max(10.0, min(60.0, 100.0 - (home_win + away_win) / 2))

    home_rpg = _safe_mean(df_home, ["rpg", "power_index", "rating"], home_win / 25.0)
    away_rpg = _safe_mean(df_away, ["rpg", "power_index", "rating"], away_win / 25.0)

    return {
        "probabilities": {
            "home_win": round(home_win, 1),
            "draw": round(draw, 1),
            "away_win": round(away_win, 1),
        },
        "strength": {
            "home_rpg": round(home_rpg, 2),
            "away_rpg": round(away_rpg, 2),
            "rpg_diff": round(home_rpg - away_rpg, 2),
        },
    }


def analyze_asian_markets(
    df_home: pd.DataFrame, df_away: pd.DataFrame, home_team: str, away_team: str
) -> List[Dict[str, Any]]:
    """
    Retorna uma lista com ATÉ 2 mercados asiáticos,
    cada um com sugestão ousada e conservadora, no formato
    esperado pelo componente AnalysisResults do painel:

    [
        {
            "market_name": "Handicap Asiático FT",
            "suggestions": {
                "ousada": { line, reason, explanation },
                "conservadora": { line, reason, explanation }
            }
        },
        ...
    ]
    """

    # Probabilidades básicas e força (RPG)
    home_win = _safe_mean(df_home, ["win_rate", "home_win_rate"], 50.0)
    away_win = _safe_mean(df_away, ["win_rate", "away_win_rate"], 50.0)
    home_rpg = _safe_mean(df_home, ["rpg", "power_index", "rating"], home_win / 25.0)
    away_rpg = _safe_mean(df_away, ["rpg", "power_index", "rating"], away_win / 25.0)
    rpg_diff = home_rpg - away_rpg

    # Tendência de gols FT
    home_over15 = _safe_mean(df_home, ["over15", "over_1_5_ft", "ft_over_1_5"], 70.0)
    away_over15 = _safe_mean(df_away, ["over15", "over_1_5_ft", "ft_over_1_5"], 70.0)
    home_over25 = _safe_mean(df_home, ["over25", "over_2_5_ft", "ft_over_2_5"], 50.0)
    away_over25 = _safe_mean(df_away, ["over25", "over_2_5_ft", "ft_over_2_5"], 50.0)

    over15 = (home_over15 + away_over15) / 2.0
    over25 = (home_over25 + away_over25) / 2.0

    # BTTS (ambas marcam)
    home_btts = _safe_mean(df_home, ["btts_yes", "btts"], 50.0)
    away_btts = _safe_mean(df_away, ["btts_yes", "btts"], 50.0)
    btts = (home_btts + away_btts) / 2.0

    # Tendência de gols HT (se existir) ou proxy baseado em FT
    home_over05_ht = _safe_mean(
        df_home,
        ["over_0_5_ht", "ht_over_0_5", "over05ht"],
        max(55.0, over15 - 10.0),
    )
    away_over05_ht = _safe_mean(
        df_away,
        ["over_0_5_ht", "ht_over_0_5", "over05ht"],
        max(55.0, over15 - 10.0),
    )
    over05_ht = (home_over05_ht + away_over05_ht) / 2.0

    markets: List[Dict[str, Any]] = []

    # ========= SCORING DOS 4 MERCADOS PRINCIPAIS =========

    # 1) Handicap Asiático FT
    fav_is_home = rpg_diff >= 0
    strength_gap = abs(rpg_diff)
    win_gap = home_win - away_win
    handicap_score = strength_gap * 20.0 + abs(win_gap) * 0.6

    # 2) Gol Asiático FT
    goals_score_ft = (over25 - 55.0) * 1.2 + (btts - 50.0) * 0.7

    # 3) Handicap Asiático HT
    handicap_ht_score = handicap_score * 0.6 + (over05_ht - 60.0) * 0.5

    # 4) Gol Asiático HT
    goals_score_ht = (over05_ht - 60.0) * 1.3 + (over15 - 70.0) * 0.4

    candidate_markets = []

    # ---------- Mercado 1: Handicap Asiático FT ----------
    if handicap_score > 5:
        if fav_is_home:
            fav = home_team
            dog = away_team
        else:
            fav = away_team
            dog = home_team

        # Linhas sugeridas
        if strength_gap >= 0.5:
            ousada = {
                "line": f"{fav} -1.0 AH (FT)",
                "reason": (
                    f"{fav} mostra força superior (diferença de RPG {strength_gap:.2f}) "
                    f"e maior probabilidade de vitória."
                ),
                "explanation": (
                    "Vitória por 2+ gols = Ganha
"
                    "Vitória por 1 gol = Push (aposta devolvida)
"
                    "Empate ou derrota = Perde"
                ),
            }
            conservadora = {
                "line": f"{fav} -0.25 AH (FT)",
                "reason": (
                    f"{fav} favorito, mas jogo pode ter equilíbrio em alguns momentos. "
                    "Linha -0.25 reduz o risco."
                ),
                "explanation": (
                    "Vitória = Ganha
"
                    "Empate = Meio red (metade perdida, metade devolvida)
"
                    "Derrota = Perde"
                ),
            }
        else:
            # Força mais equilibrada → proteção maior
            ousada = {
                "line": f"{fav} 0.0 AH (FT)",
                "reason": (
                    "Jogo equilibrado, mas com leve vantagem de força para o favorito. "
                    "Linha de empate devolve."
                ),
                "explanation": (
                    "Vitória = Ganha
"
                    "Empate = Push (aposta devolvida)
"
                    "Derrota = Perde"
                ),
            }
            conservadora = {
                "line": f"{dog} +0.5 AH (FT)",
                "reason": (
                    f"Força próxima (diferença de RPG {strength_gap:.2f}). "
                    f"{dog} pode segurar empate."
                ),
                "explanation": (
                    "Vitória ou empate do time +0.5 = Ganha
"
                    "Derrota por 1+ gol = Perde"
                ),
            }

        candidate_markets.append(
            {
                "market_name": "Handicap Asiático FT",
                "score": handicap_score,
                "suggestions": {
                    "ousada": ousada,
                    "conservadora": conservadora,
                },
            }
        )

    # ---------- Mercado 2: Gol Asiático FT ----------
    if goals_score_ft > 0:
        if over25 >= 72:
            ousada = {
                "line": "Over 2.75 gols (FT)",
                "reason": (
                    f"Altíssima tendência de gols (Over 2.5 ~ {over25:.0f}%) "
                    "e cenário ofensivo forte para ambos."
                ),
                "explanation": (
                    "4+ gols = Ganha
"
                    "3 gols = Meio green (metade ganha, metade devolvida)
"
                    "0-2 gols = Perde"
                ),
            }
            conservadora = {
                "line": "Over 2.0 gols (FT)",
                "reason": (
                    "Mercado de linha inteira com proteção em caso de partida truncada."
                ),
                "explanation": (
                    "3+ gols = Ganha
"
                    "2 gols = Push (aposta devolvida)
"
                    "0-1 gol = Perde"
                ),
            }
        elif over25 >= 60:
            ousada = {
                "line": "Over 2.5 gols (FT)",
                "reason": (
                    f"Tendência positiva para gols (Over 2.5 ~ {over25:.0f}%). "
                    "Jogo com bom ritmo ofensivo."
                ),
                "explanation": (
                    "3+ gols = Ganha
"
                    "0-2 gols = Perde"
                ),
            }
            conservadora = {
                "line": "Over 1.75 gols (FT)",
                "reason": (
                    "Linha mais baixa para proteger em caso de jogo com poucos gols."
                ),
                "explanation": (
                    "3+ gols = Ganha
"
                    "2 gols = Meio green (metade ganha, metade devolvida)
"
                    "0-1 gol = Perde"
                ),
            }
        else:
            ousada = {
                "line": "Over 2.0 gols (FT)",
                "reason": (
                    "Cenário intermediário: possibilidade de 2-3 gols, "
                    "mas sem padrão tão forte de over."
                ),
                "explanation": (
                    "3+ gols = Ganha
"
                    "2 gols = Push (devolvida)
"
                    "0-1 gol = Perde"
                ),
            }
            conservadora = {
                "line": "Over 1.5 gols (FT)",
                "reason": (
                    "Proteção para jogos mais amarrados, buscando apenas 2 gols na partida."
                ),
                "explanation": (
                    "2+ gols = Ganha
"
                    "0-1 gol = Perde"
                ),
            }

        candidate_markets.append(
            {
                "market_name": "Gol Asiático FT",
                "score": goals_score_ft,
                "suggestions": {
                    "ousada": ousada,
                    "conservadora": conservadora,
                },
            }
        )

    # ---------- Mercado 3: Handicap Asiático HT ----------
    if handicap_ht_score > 0:
        fav_ht = home_team if fav_is_home else away_team
        dog_ht = away_team if fav_is_home else home_team

        ousada = {
            "line": f"{fav_ht} -0.5 AH (HT)",
            "reason": (
                f"{fav_ht} tende a começar melhor, com maior força (RPG {home_rpg:.2f} x {away_rpg:.2f}) "
                "e boa chance de liderar no intervalo."
            ),
            "explanation": (
                "Vencendo no HT = Ganha
"
                "Empate ou perdendo no HT = Perde"
            ),
        }
        conservadora = {
            "line": f"{dog_ht} +0.25 AH (HT)",
            "reason": (
                "Proteção para 1º tempo equilibrado, onde o time azarão pode segurar empate."
            ),
            "explanation": (
                "Vencendo no HT = Ganha
"
                "Empate = Meio green / devolução parcial
"
                "Perdendo = Perde"
            ),
        }

        candidate_markets.append(
            {
                "market_name": "Handicap Asiático HT",
                "score": handicap_ht_score,
                "suggestions": {
                    "ousada": ousada,
                    "conservadora": conservadora,
                },
            }
        )

    # ---------- Mercado 4: Gol Asiático HT ----------
    if goals_score_ht > 0:
        if over05_ht >= 70:
            ousada = {
                "line": "Over 1.25 gols (HT)",
                "reason": (
                    f"1º tempo com forte padrão ofensivo (Over 0.5 HT ~ {over05_ht:.0f}%)."
                ),
                "explanation": (
                    "2+ gols no HT = Ganha
"
                    "1 gol no HT = Meio green
"
                    "0 gols no HT = Perde"
                ),
            }
            conservadora = {
                "line": "Over 0.75 gols (HT)",
                "reason": (
                    "Linha agressiva mas ainda com proteção parcial em caso de apenas 1 gol."
                ),
                "explanation": (
                    "2+ gols no HT = Ganha
"
                    "1 gol no HT = Meio green
"
                    "0 gols no HT = Perde"
                ),
            }
        else:
            ousada = {
                "line": "Over 1.0 gol (HT)",
                "reason": (
                    "Cenário intermediário para gols no 1º tempo – há risco de terminar 0x0."
                ),
                "explanation": (
                    "2+ gols no HT = Ganha
"
                    "1 gol no HT = Push (devolvida)
"
                    "0 gols no HT = Perde"
                ),
            }
            conservadora = {
                "line": "Over 0.5 gol (HT)",
                "reason": (
                    "Abordagem conservadora, buscando apenas 1 gol no 1º tempo."
                ),
                "explanation": (
                    "1+ gol no HT = Ganha
"
                    "0 gols no HT = Perde"
                ),
            }

        candidate_markets.append(
            {
                "market_name": "Gol Asiático HT",
                "score": goals_score_ht,
                "suggestions": {
                    "ousada": ousada,
                    "conservadora": conservadora,
                },
            }
        )

    # Ordena por score e retorna apenas os 2 melhores mercados
    if not candidate_markets:
        return []

    top = sorted(candidate_markets, key=lambda m: m.get("score", 0), reverse=True)[:2]

    # Remove chave interna "score" antes de enviar para o frontend
    for m in top:
        m.pop("score", None)

    return top
