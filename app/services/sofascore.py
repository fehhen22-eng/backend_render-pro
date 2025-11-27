import aiohttp
from typing import Optional, Dict, List
from datetime import datetime
import pandas as pd
from config.settings import settings
from app.utils.file_manager import save_team_data
from utils.team_normalizer import slugify


class SofascoreService:
    """Serviço para buscar e atualizar estatísticas do Sofascore."""
    
    def __init__(self):
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

                async with session.get(search_url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        for item in data.get("results", []):
                            if item.get("type") == "team":
                                entity = item.get("entity", {})
                                return entity.get("id")
        except:
            pass
        
        return None
    

    async def get_team_matches(self, team_id: int, limit: int = 20) -> List[Dict]:
        """
        Busca últimas partidas do time com estatísticas base.
        """
        matches = []

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/team/{team_id}/events/last/{limit}"

                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        for event in data.get("events", []):
                            md = await self._parse_match(event)
                            if md:
                                matches.append(md)
        except Exception as e:
            print("Erro get_team_matches:", e)

        return matches
    

    async def _parse_match(self, event: Dict) -> Optional[Dict]:
        """
        Processa informações básicas e estatísticas da partida.
        """
        try:
            event_id = event.get("id")
            match = {
                "date": datetime.fromtimestamp(event["startTimestamp"]).strftime("%Y-%m-%d"),
                "home_team": event["homeTeam"]["name"],
                "away_team": event["awayTeam"]["name"],
                "home_goals": event["homeScore"]["current"],
                "away_goals": event["awayScore"]["current"],
            }

            # Stats detalhadas
            stats = await self.get_match_statistics(event_id)
            match.update(stats)

            return match

        except Exception as e:
            print("Erro _parse_match:", e)
            return None
    

    async def get_match_statistics(self, event_id: int) -> Dict:
        """
        Estatísticas avançadas: escanteios, chutes, cartões.
        """
        stats = {
            "home_corners": 0,
            "away_corners": 0,
            "home_shots": 0,
            "away_shots": 0,
            "home_target": 0,
            "away_target": 0,
            "home_yellow": 0,
            "away_yellow": 0,
            "home_red": 0,
            "away_red": 0
        }

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/event/{event_id}/statistics"

                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        for group in data.get("statistics", []):
                            for g in group.get("groups", []):
                                for item in g.get("statisticsItems", []):
                                    name = item["name"].lower()

                                    if "corner" in name:
                                        stats["home_corners"] = item["homeValue"]
                                        stats["away_corners"] = item["awayValue"]

                                    elif "total shots" in name:
                                        stats["home_shots"] = item["homeValue"]
                                        stats["away_shots"] = item["awayValue"]

                                    elif "shots on target" in name:
                                        stats["home_target"] = item["homeValue"]
                                        stats["away_target"] = item["awayValue"]

                                    elif "yellow" in name:
                                        stats["home_yellow"] = item["homeValue"]
                                        stats["away_yellow"] = item["awayValue"]

                                    elif "red" in name:
                                        stats["home_red"] = item["homeValue"]
                                        stats["away_red"] = item["awayValue"]

        except Exception as e:
            print("Erro get_match_statistics:", e)

        return stats
    

    async def update_team_csv(self, league_id: str, team_id: str, team_name: str) -> bool:
        """
        Atualiza o CSV do time com dados completos + estatísticas do Sofascore.
        """
        try:
            sofascore_id = await self.get_team_id(team_name)

            if not sofascore_id:
                print(f"Time não encontrado no SofaScore: {team_name}")
                return False
            
            matches = await self.get_team_matches(sofascore_id, limit=30)

            if not matches:
                print(f"Nenhuma partida encontrada para {team_name}")
                return False

            df = pd.DataFrame(matches)

            # salva realmente o CSV do time
            team_slug = slugify(team_name)
            return save_team_data(league_id, team_slug, df)

        except Exception as e:
            print("Erro update_team_csv:", e)
            return False


# Instância global
sofascore_service = SofascoreService()
