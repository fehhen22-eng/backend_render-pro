from fastapi import APIRouter
from app.services.h2h_analyzer import H2HAnalyzer

router = APIRouter()
analyzer = H2HAnalyzer()


@router.get("/{league_id}/{team1_id}/{team2_id}")
def analyze_h2h(league_id: str, team1_id: str, team2_id: str):
    """
    Endpoint H2H completo.
    """
    result = analyzer.analyze_h2h(league_id, team1_id, team2_id)
    return result
