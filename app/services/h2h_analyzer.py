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
        # Normaliza o team_id diretamente para garantir consistência
        team_normalized = normalize_team_name(team_id)
        
        # Inicializa estatísticas
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
        
        # Processa cada partida
        for _, match in df.iterrows():
            # Normaliza os nomes dos times do CSV para comparação consistente
            home_team_normalized = normalize_team_name(str(match.get("home_team", "")))
            away_team_normalized = normalize_team_name(str(match.get("away_team", "")))
            
            home_goals = int(match.get("home_goals", 0) or 0)
            away_goals = int(match.get("away_goals", 0) or 0)
            
            # Determina se o time jogou em casa, fora, ou não participou desta partida
            # Usa substring match para lidar com sufixos (ex: "Real Madrid" vs "Real Madrid CF")
            is_home = team_normalized in home_team_normalized or home_team_normalized in team_normalized
            is_away = team_normalized in away_team_normalized or away_team_normalized in team_normalized
            
            # Pula partidas onde o time não participou
            if not is_home and not is_away:
                continue
            
            # Se o time aparece em ambos (raro mas possível em amistosos), prioriza home
            if is_home and is_away:
                is_away = False
            
            # Conta a partida
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
        
        # Calcula médias
        if stats["matches_played"] > 0:
            stats["avg_goals_scored"] = round(stats["goals_scored"] / stats["matches_played"], 2)
            stats["avg_goals_conceded"] = round(stats["goals_conceded"] / stats["matches_played"], 2)
            stats["avg_corners_for"] = round(stats["corners_for"] / stats["matches_played"], 2)
            stats["avg_corners_against"] = round(stats["corners_against"] / stats["matches_played"], 2)
            stats["avg_shots_for"] = round(stats["shots_for"] / stats["matches_played"], 2)
            stats["avg_shots_against"] = round(stats["shots_against"] / stats["matches_played"], 2)
            stats["avg_yellow_cards"] = round(stats["yellow_cards"] / stats["matches_played"], 2)
        
        return stats
    
    def _calculate_probabilities(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula probabilidades de vitória, empate e derrota."""
        total_matches = team1_stats["matches_played"] + team2_stats["matches_played"]
        
        if total_matches == 0:
            return {"team1_win": 33.33, "draw": 33.33, "team2_win": 33.33}
        
        # Força dos times baseada em vitórias e diferença de gols
        team1_strength = (
            team1_stats["wins"] * 3 + 
            team1_stats["draws"] * 1 +
            (team1_stats["goals_scored"] - team1_stats["goals_conceded"])
        )
        
        team2_strength = (
            team2_stats["wins"] * 3 + 
            team2_stats["draws"] * 1 +
            (team2_stats["goals_scored"] - team2_stats["goals_conceded"])
        )
        
        total_strength = team1_strength + team2_strength
        
        if total_strength == 0:
            return {"team1_win": 33.33, "draw": 33.33, "team2_win": 33.33}
        
        # Calcula probabilidades básicas
        team1_prob = (team1_strength / total_strength) * 100
        team2_prob = (team2_strength / total_strength) * 100
        
        # Ajusta para incluir probabilidade de empate
        draw_prob = 25.0  # Base de 25% para empate
        team1_prob = team1_prob * 0.75
        team2_prob = team2_prob * 0.75
        
        return {
            "team1_win": round(team1_prob, 2),
            "draw": round(draw_prob, 2),
            "team2_win": round(team2_prob, 2)
        }
    
    def _calculate_over_under(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula probabilidades de Over/Under."""
        avg_goals = team1_stats.get("avg_goals_scored", 0) + team2_stats.get("avg_goals_scored", 0)
        
        return {
            "total_expected_goals": round(avg_goals, 2),
            "over_1_5": round(min(95, avg_goals * 35), 2),
            "over_2_5": round(min(90, avg_goals * 25), 2),
            "over_3_5": round(min(80, avg_goals * 15), 2),
            "under_2_5": round(max(10, 100 - avg_goals * 25), 2),
            "under_3_5": round(max(20, 100 - avg_goals * 15), 2),
        }
    
    def _calculate_btts(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula probabilidade de Both Teams To Score."""
        team1_scoring = team1_stats.get("avg_goals_scored", 0)
        team2_scoring = team2_stats.get("avg_goals_scored", 0)
        
        btts_prob = min(95, (team1_scoring + team2_scoring) * 30)
        
        return {
            "btts_yes": round(btts_prob, 2),
            "btts_no": round(100 - btts_prob, 2)
        }
    
    def _calculate_corners(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula estatísticas de escanteios."""
        avg_corners = team1_stats.get("avg_corners_for", 0) + team2_stats.get("avg_corners_for", 0)
        
        return {
            "total_expected_corners": round(avg_corners, 2),
            "over_8_5": round(min(95, avg_corners * 8), 2),
            "over_9_5": round(min(90, avg_corners * 7), 2),
            "over_10_5": round(min(85, avg_corners * 6), 2),
            "under_9_5": round(max(10, 100 - avg_corners * 7), 2),
            "under_10_5": round(max(15, 100 - avg_corners * 6), 2),
        }
    
    def _calculate_shots(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula estatísticas de chutes."""
        avg_shots = team1_stats.get("avg_shots_for", 0) + team2_stats.get("avg_shots_for", 0)
        
        return {
            "total_expected_shots": round(avg_shots, 2),
            "team1_avg_shots": team1_stats.get("avg_shots_for", 0),
            "team2_avg_shots": team2_stats.get("avg_shots_for", 0),
        }
    
    def _calculate_cards(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula estatísticas de cartões."""
        avg_cards = team1_stats.get("avg_yellow_cards", 0) + team2_stats.get("avg_yellow_cards", 0)
        
        return {
            "total_expected_cards": round(avg_cards, 2),
            "over_3_5": round(min(90, avg_cards * 20), 2),
            "over_4_5": round(min(85, avg_cards * 15), 2),
            "under_4_5": round(max(15, 100 - avg_cards * 15), 2),
        }
    
    def _calculate_asian_handicap(self, team1_stats: Dict, team2_stats: Dict) -> Dict:
        """Calcula sugestões de Handicap Asiático."""
        goal_diff = team1_stats.get("avg_goals_scored", 0) - team2_stats.get("avg_goals_scored", 0)
        corner_diff = team1_stats.get("avg_corners_for", 0) - team2_stats.get("avg_corners_for", 0)
        
        # Handicap de gols
        if abs(goal_diff) < 0.3:
            goal_handicap_conservative = "0.0"
            goal_handicap_bold = "0.5"
        elif abs(goal_diff) < 0.7:
            goal_handicap_conservative = "0.5"
            goal_handicap_bold = "1.0"
        else:
            goal_handicap_conservative = "1.0"
            goal_handicap_bold = "1.5"
        
        # Handicap de escanteios
        if abs(corner_diff) < 0.5:
            corner_handicap_conservative = "0.0"
            corner_handicap_bold = "1.5"
        elif abs(corner_diff) < 1.5:
            corner_handicap_conservative = "1.5"
            corner_handicap_bold = "2.5"
        else:
            corner_handicap_conservative = "2.5"
            corner_handicap_bold = "3.5"
        
        return {
            "goals": {
                "conservative": goal_handicap_conservative,
                "bold": goal_handicap_bold,
                "favorite": "team1" if goal_diff > 0 else "team2"
            },
            "corners": {
                "conservative": corner_handicap_conservative,
                "bold": corner_handicap_bold,
                "favorite": "team1" if corner_diff > 0 else "team2"
            }
        }


# Instância global do analisador
h2h_analyzer = H2HAnalyzer()
