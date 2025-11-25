import aiohttp
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
from datetime import datetime
import pandas as pd
from config.settings import settings


class SofascoreService:
    """Serviço para buscar dados do Sofascore."""
    
    def __init__(self):
        self.base_url = settings.SOFASCORE_BASE_URL
        self.api_url = settings.SOFASCORE_API_URL
        self.headers = settings.DEFAULT_HEADERS
    
    async def get_team_id(self, team_name: str) -> Optional[int]:
        """
        Busca o ID do time no Sofascore.
        """
        try:
            async with aiohttp.ClientSession() as session:
                search_url = f"{self.api_url}/search/all"
                params = {"q": team_name}
                
                async with session.get(
                    search_url,
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Procura pelo time nos resultados
                        if "results" in data:
                            for result in data["results"]:
                                if result.get("type") == "team":
                                    return result.get("entity", {}).get("id")
        
        except Exception as e:
            print(f"Erro ao buscar ID do time {team_name}: {e}")
        
        return None
    
    async def get_team_matches(
        self,
        team_id: int,
        limit: int = 20
    ) -> List[Dict]:
        """
        Busca as últimas partidas de um time.
        """
        matches = []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/team/{team_id}/events/last/{limit}"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        events = data.get("events", [])
                        
                        for event in events:
                            match_data = await self._parse_match(event)
                            if match_data:
                                matches.append(match_data)
        
        except Exception as e:
            print(f"Erro ao buscar partidas do time {team_id}: {e}")
        
        return matches
    
    async def _parse_match(self, event: Dict) -> Optional[Dict]:
        """
        Processa os dados de uma partida.
        """
        try:
            home_team = event.get("homeTeam", {})
            away_team = event.get("awayTeam", {})
            home_score = event.get("homeScore", {})
            away_score = event.get("awayScore", {})
            
            match_data = {
                "date": datetime.fromtimestamp(event.get("startTimestamp", 0)).strftime("%Y-%m-%d"),
                "home_team": home_team.get("name", ""),
                "away_team": away_team.get("name", ""),
                "home_goals": home_score.get("current", 0),
                "away_goals": away_score.get("current", 0),
                "tournament": event.get("tournament", {}).get("name", ""),
            }
            
            # Busca estatísticas detalhadas se disponível
            event_id = event.get("id")
            if event_id:
                stats = await self.get_match_statistics(event_id)
                match_data.update(stats)
            
            return match_data
        
        except Exception as e:
            print(f"Erro ao processar partida: {e}")
            return None
    
    async def get_match_statistics(self, event_id: int) -> Dict:
        """
        Busca estatísticas detalhadas de uma partida.
        """
        stats = {
            "home_corners": 0,
            "away_corners": 0,
            "home_shots": 0,
            "away_shots": 0,
            "home_shots_on_target": 0,
            "away_shots_on_target": 0,
            "home_yellow_cards": 0,
            "away_yellow_cards": 0,
            "home_red_cards": 0,
            "away_red_cards": 0,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/event/{event_id}/statistics"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Processa as estatísticas
                        statistics = data.get("statistics", [])
                        for stat_group in statistics:
                            groups = stat_group.get("groups", [])
                            for group in groups:
                                stats_items = group.get("statisticsItems", [])
                                for item in stats_items:
                                    stat_name = item.get("name", "").lower()
                                    home_value = item.get("homeValue", 0)
                                    away_value = item.get("awayValue", 0)
                                    
                                    if "corner" in stat_name:
                                        stats["home_corners"] = home_value
                                        stats["away_corners"] = away_value
                                    elif "total shots" in stat_name:
                                        stats["home_shots"] = home_value
                                        stats["away_shots"] = away_value
                                    elif "shots on target" in stat_name:
                                        stats["home_shots_on_target"] = home_value
                                        stats["away_shots_on_target"] = away_value
                                    elif "yellow card" in stat_name:
                                        stats["home_yellow_cards"] = home_value
                                        stats["away_yellow_cards"] = away_value
                                    elif "red card" in stat_name:
                                        stats["home_red_cards"] = home_value
                                        stats["away_red_cards"] = away_value
        
        except Exception as e:
            print(f"Erro ao buscar estatísticas da partida {event_id}: {e}")
        
        return stats
    
    async def update_team_csv(
        self,
        league_id: str,
        team_id: str,
        team_name: str
    ) -> bool:
        """
        Atualiza o CSV de um time com dados do Sofascore.
        """
        from app.utils.file_manager import save_team_data
        
        # Busca o ID do time no Sofascore
        sofascore_id = await self.get_team_id(team_name)
        
        if not sofascore_id:
            print(f"ID do time {team_name} não encontrado no Sofascore")
            return False
        
        # Busca as partidas
        matches = await self.get_team_matches(sofascore_id, limit=30)
        
        if not matches:
            print(f"Nenhuma partida encontrada para {team_name}")
            return False
        
        # Cria DataFrame e salva
        df = pd.DataFrame(matches)
        return save_team_data(league_id, team_id, df)


# Instância global do serviço
sofascore_service = SofascoreService()
