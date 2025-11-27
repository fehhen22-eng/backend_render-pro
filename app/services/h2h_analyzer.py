import pandas as pd
from typing import Dict, Optional, Tuple
from app.utils.file_manager import load_team_data
from app.utils.team_normalizer import normalize_team_name


class H2HAnalyzer:
    """Analisador de confrontos diretos (Head to Head)."""

    def analyze_h2h(self, league_id: str, team1_id: str, team2_id: str) -> Dict:
        """
        Faz análise do confronto H2H entre dois times.
        """

        # Carrega dados CSV dos times
        df1 = load_team_data(league_id, team1_id)
        df2 = load_team_data(league_id, team2_id)

        if df1 is None or df2 is None:
            return {"error": "Dados de um ou ambos os times não encontrados."}

        # Processamento de estatísticas
        team1_stats = self._calculate_team_stats(df1, team1_id)
        team2_stats = self._calculate_team_stats(df2, team2_id)

        # Probabilidades
        probabilities = self._calculate_probabilities(team1_stats, team2_stats)

        # Over/Under
        over_under = self._calculate_over_under(team1_stats, team2_stats)

        # BTTS
        btts = self._calculate_btts(team1_stats, team2_stats)

        return {
            "teams": {
                "team1": team1_stats,
                "team2": team2_stats
            },
            "probabilities": probabilities,
            "over_under": over_under,
            "btts": btts
        }

    # ---------------------------------------------
    # FUNÇÕES INTERNAS
    # ---------------------------------------------

    def _calculate_team_stats(self, df: pd.DataFrame, team_id: str) -> Dict:
        """Cálculo simples de estatísticas do time."""
        total_jogos = len(df)
        avg_gf = df["gf"].mean() if "gf" in df else 0
        avg_ga = df["ga"].mean() if "ga" in df else 0

        return {
            "team_id": team_id,
            "games": total_jogos,
            "avg_gf": round(avg_gf, 2),
            "avg_ga": round(avg_ga, 2),
        }

    def _calculate_probabilities(self, t1: Dict, t2: Dict) -> Dict:
        """Cálculo básico de probabilidade por média de gols."""
        total = (t1["avg_gf"] + t2["avg_gf"]) or 1
        p1 = t1["avg_gf"] / total
        p2 = t2["avg_gf"] / total

        return {
            "home_win": round(p1 * 100, 2),
            "away_win": round(p2 * 100, 2),
            "draw": 100 - round((p1 + p2) * 100, 2)
        }

    def _calculate_over_under(self, t1: Dict, t2: Dict) -> Dict:
        media = t1["avg_gf"] + t2["avg_gf"]
        return {
            "over_1_5": media > 1.5,
            "over_2_5": media > 2.5,
        }

    def _calculate_btts(self, t1: Dict, t2: Dict) -> bool:
        return (t1["avg_gf"] > 1.0) and (t2["avg_gf"] > 1.0)
