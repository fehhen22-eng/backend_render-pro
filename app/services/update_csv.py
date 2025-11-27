import asyncio
from datetime import datetime, timedelta
from typing import Dict
from app.utils.file_manager import list_leagues, list_teams, save_team_csv
from app.services.sofascore import sofascore_service
from utils.team_normalizer import slugify


class CSVUpdateService:
    """Serviço para atualização automática dos CSVs."""
    
    def __init__(self):
        self.update_interval_hours = 48
        self.last_update = None
    
    async def should_update(self) -> bool:
        """Verifica se deve atualizar os dados."""
        if self.last_update is None:
            return True
        
        time_since_update = datetime.now() - self.last_update
        return time_since_update >= timedelta(hours=self.update_interval_hours)
    

    async def update_all_teams(self) -> Dict:
        """
        Atualiza todos os times de todas as ligas.
        """
        results = {"updated": [], "failed": []}

        leagues = list_leagues()

        for league in leagues:
            league_id = league["league_id"]

            teams = list_teams(league_id)

            for team in teams:
                team_id = team["team_id"]
                team_name = team["name"]

                try:
                    # baixa dados do Sofascore
                    df = await sofascore_service.get_team_stats(team_name)

                    # salva o CSV atualizado
                    filename = slugify(team_name) + ".csv"
                    save_team_csv(league_id, filename, df.to_csv(index=False).encode())

                    results["updated"].append(f"{league_id}/{team_id}")

                except Exception as e:
                    results["failed"].append({
                        "team": f"{league_id}/{team_id}",
                        "error": str(e)
                    })

                await asyncio.sleep(1)

        self.last_update = datetime.now()
        return results
    

    async def update_league(self, league_id: str) -> Dict:
        results = {"updated": [], "failed": []}

        teams = list_teams(league_id)

        for team in teams:
            team_id = team["team_id"]
            team_name = team["name"]

            try:
                df = await sofascore_service.get_team_stats(team_name)

                filename = slugify(team_name) + ".csv"
                save_team_csv(league_id, filename, df.to_csv(index=False).encode())

                results["updated"].append(team_id)

            except Exception as e:
                results["failed"].append({
                    "team": team_id,
                    "error": str(e)
                })

            await asyncio.sleep(1)

        return results
    

    async def update_team(self, league_id: str, team_id: str) -> bool:
        """
        Atualiza um único time.
        """
        try:
            team_name = team_id.replace("-", " ").title()
            df = await sofascore_service.get_team_stats(team_name)

            filename = slugify(team_name) + ".csv"
            save_team_csv(league_id, filename, df.to_csv(index=False).encode())

            return True

        except Exception as e:
            print(f"Erro ao atualizar {league_id}/{team_id}: {e}")
            return False


# Instância global
update_service = CSVUpdateService()
