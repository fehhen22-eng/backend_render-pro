import pandas as pd
from typing import Dict, List, Optional, Tuple
from app.utils.file_manager import load_team_data

from app.utils.team_normalizer import normalize_team_name


class H2HAnalyzer:
    """Analisador de confrontos diretos (Head to Head)."""
    
    def analyze_h2h(
        self,
        league_id: str,
        team1_id: str,
        team2_id: str
    ) -> Dict:
        """
        Analisa o confronto entre dois times.
        """
        # Carrega dados dos times
        df1 = load_team_data(league_id, team1_id)
        df2 = load_team_data(league_id, team2_id)
        
        if df1 is None or df2 is None:
            return {
                "error": "Dados de um ou ambos os times não encontrados"
            }
        
        # Análise geral
        team1_stats = self._calculate_team_stats(df1, team1_id)
        team2_stats = self._calculate_team_stats(df2, team2_id)
        
        # Probabilidades
        probabilities = self._calculate_probabilities(team1_stats, team2_stats)
        
        # Over/Under
        over_under = self._calculate_over_under(team1_stats, team2_stats)
        
        # BTTS (Both Teams To Score)
        btts = self._calculate_btts(team1_stats, team2_stats)
        
        # Escanteios
        corners = self._calculate_corners(team1_stats, team2_stats)
        
        # Chutes
        shots = self._calculate_shots(team1_stats, team2_stats)
        
        # Cartões
        cards = self._calculate_cards(team1_stats, team2_stats)
        
        # Handicap Asiático
        asian_handicap = self._calculate_asian_handicap(team1_stats, team2_stats)
        
        return {
            "team1": {
                "id": team1_id,
                "name": team1_id.replace("-", " ").title(),
                "stats": team1_stats
            },
            "team2": {
                "id": team2_id,
                "name": team2_id.replace("-", " ").title(),
                "stats": team2_stats
            },
            "probabilities": probabilities,
            "over_under": over_under,
            "btts": btts,
            "corners": corners,
            "shots": shots,
            "cards": cards,
            "asian_handicap": asian_handicap
        }
    
    def _calculate_team_stats(self, df: pd.DataFrame, team_id: str) -> Dict:
        """Calcula estatísticas de um time."""
        team_normalized = normalize_team_name(team_id)
        
        stats = {
            "matches_played": 0,
            "goals_scored": 0,
            "goals_conceded": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "corners_for": 0,
            "corners_against": 0,
            "shots_for": 0,
            "shots_against": 0,
            "shots_on_target_for": 0,
            "shots_on_target_against": 0,
            "yellow_cards": 0,
            "red_cards": 0,
        }
        
        for _, match in df.iterrows():
            home_team_normalized = normalize_team_name(str(match.get("home_team", "")))
            away_team_normalized = normalize_team_name(str(match.get("away_team", "")))
            
            home_goals = int(match.get("home_goals", 0) or 0)
            away_goals = int(match.get("away_goals", 0) or 0)
            
            is_home = team_normalized in home_team_normalized or home_team_normalized in team_normalized
            is_away = team_normalized in away_team_normalized or away_team_normalized in team_normalized
            
            if not is_home and not is_away:
                continue
            
            if is_home and is_away:
                is_away = False
            
            stats["matches_played"] += 1
            
            if is_home:
                stats["goals_scored"] += home_goals
                stats["goals_conceded"] += away_goals
                stats["corners_for"] += int(match.get("home_corners", 0) or 0)
                stats["corners_against"] += int(match.get("away_corners", 0) or 0)
                stats["shots_for"] += int(match.get("home_shots", 0) or 0)
                stats["shots_against"] += int(match.get("away_shots", 0) or 0)
                stats["shots_on_target_for"] += int(match.get("home_shots_on_target", 0) or 0)
                stats["shots_on_target_against"] += int(match.get("away_shots_on_target", 0) or 0)
                stats["yellow_cards"] += int(match.get("home_yellow_cards", 0) or 0)
                stats["red_cards"] += int(match.get("home_red_cards", 0) or 0)
                
                if home_goals > away_goals:
                    stats["wins"] += 1
                elif home_goals == away_goals:
                    stats["draws"] += 1
                else:
                    stats["losses"] += 1
            else:
                stats["goals_scored"] += away_goals
                stats["goals_conceded"] += home_goals
                stats["corners_for"] += int(match.get("away_corners", 0) or 0)
                stats["corners_against"] += int(match.get("home_corners", 0) or 0)
                stats["shots_for"] += int(match.get("away_shots", 0) or 0)
                stats["shots_against"] += int(match.get("home_shots", 0) or 0)
                stats["shots_on_target_for"] += int(match.get("away_shots_on_target", 0) or 0)
                stats["shots_on_target_against"] += int(match.get("home_shots_on_target", 0) or 0)
                stats["yellow_cards"] += int(match.get("away_yellow_cards", 0) or 0)
                stats["red_cards"] += int(match.get("away_red_cards", 0) or 0)
                
                if away_goals > home_goals:
                    stats["wins"] += 1
                elif away_goals == home_goals:
                    stats["draws"] += 1
                else:
                    stats["losses"] += 1
        
        if stats["matches_played"] > 0:
            stats["avg_goals_scored"] = round(stats["goals_scored"] / stats["matches_played"], 2)
            stats["avg_goals_conceded"] = round(stats["goals_conceded"] / stats["matches_played"], 2)
            stats["avg_corners_for"] = round(stats["corners_for"] / stats["matches_played"], 2)
            stats["avg_corners_against"] = round(stats["corners_against"] / stats["matches_played"], 2)
            stats["avg_shots_for"] = round(stats["shots_for"] / stats["matches_played"], 2)
            stats["avg_shots_against"] = round(stats["shots_against"] / stats["matches_played"], 2)
            stats["avg_yellow_cards"] = round(stats["yellow_cards"] / stats["matches_played"], 2)
        
        return stats
