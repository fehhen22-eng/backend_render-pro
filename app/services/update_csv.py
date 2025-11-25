import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from app.utils.file_manager import list_leagues, list_teams
from app.services.sofascore import sofascore_service


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
        results = {
            "updated": [],
            "failed": [],
            "skipped": []
        }
        
        # Lista todas as ligas
        leagues = list_leagues()
        
        for league in leagues:
            league_id = league["id"]
            
            # Lista todos os times da liga
            teams = list_teams(league_id)
            
            for team in teams:
                team_id = team["id"]
                team_name = team["name"]
                
                try:
                    success = await sofascore_service.update_team_csv(
                        league_id,
                        team_id,
                        team_name
                    )
                    
                    if success:
                        results["updated"].append({
                            "league": league_id,
                            "team": team_id
                        })
                    else:
                        results["failed"].append({
                            "league": league_id,
                            "team": team_id,
                            "reason": "Update returned False"
                        })
                
                except Exception as e:
                    results["failed"].append({
                        "league": league_id,
                        "team": team_id,
                        "reason": str(e)
                    })
                
                # Aguarda um pouco entre requisições para não sobrecarregar
                await asyncio.sleep(2)
        
        self.last_update = datetime.now()
        
        return results
    
    async def update_league(self, league_id: str) -> Dict:
        """
        Atualiza todos os times de uma liga específica.
        """
        results = {
            "updated": [],
            "failed": []
        }
        
        teams = list_teams(league_id)
        
        for team in teams:
            team_id = team["id"]
            team_name = team["name"]
            
            try:
                success = await sofascore_service.update_team_csv(
                    league_id,
                    team_id,
                    team_name
                )
                
                if success:
                    results["updated"].append(team_id)
                else:
                    results["failed"].append({
                        "team": team_id,
                        "reason": "Update returned False"
                    })
            
            except Exception as e:
                results["failed"].append({
                    "team": team_id,
                    "reason": str(e)
                })
            
            await asyncio.sleep(2)
        
        return results
    
    async def update_team(self, league_id: str, team_id: str) -> bool:
        """
        Atualiza um time específico.
        """
        # Converte tanto hífens quanto underscores em espaços para busca no Sofascore
        team_name = team_id.replace("-", " ").replace("_", " ").title()
        
        try:
            success = await sofascore_service.update_team_csv(
                league_id,
                team_id,
                team_name
            )
            return success
        
        except Exception as e:
            print(f"Erro ao atualizar time {team_id}: {e}")
            return False


# Instância global do serviço
update_service = CSVUpdateService()
