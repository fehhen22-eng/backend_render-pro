
import requests
from typing import Dict, Any
from ..utils.logo_cache import get_or_download_logo

BASE="https://api.sofascore.com/api/v1"

HDR={"User-Agent":"Mozilla/5.0"}

def search_team_and_get_id(team_slug:str)->Dict[str,Any]:
    q=team_slug.replace("-"," ")
    url=f"{BASE}/search/all?q={q}"
    r=requests.get(url,headers=HDR,timeout=10).json()
    teams=r.get("teams",[])
    if teams:
        t=teams[0]
        team_id = t["id"]
        # Tenta baixar/cachear o logo da equipe
        get_or_download_logo(team_id)
        return {"team_id":team_id,"team_name":t["name"]}
    return {"team_id":abs(hash(team_slug))%999999,"team_name":q.title()}

def fetch_team_stats(team_id:int)->Dict[str,float]:
    # fetch last 20 matches
    ev=requests.get(f"{BASE}/team/{team_id}/events/last/0",headers=HDR,timeout=10).json()
    events=ev.get("events",[])[:20]
    stats={"goals_scored":0,"goals_conceded":0,
           "goals_scored_ht":0,"goals_conceded_ht":0,
           "corners":0,"corners_ht":0,
           "cards":0,
           "shots_total":0,"shots_on":0}
    n=0
    for e in events:
        mid=e["id"]
        st=requests.get(f"{BASE}/event/{mid}/statistics",headers=HDR,timeout=10).json()
        g=e.get("homeScore",{}).get("current",0) if e["homeTeam"]["id"]==team_id else e.get("awayScore",{}).get("current",0)
        ga=e.get("awayScore",{}).get("current",0) if e["homeTeam"]["id"]==team_id else e.get("homeScore",{}).get("current",0)
        stats["goals_scored"]+=g
        stats["goals_conceded"]+=ga
        # simplified extraction
        for grp in st.get("statistics",[]):
            for it in grp.get("groups",[]):
                name=it.get("name","").lower()
                h=it.get("home",0) or 0
                a=it.get("away",0) or 0
                val=h if e["homeTeam"]["id"]==team_id else a
                if "corner" in name: stats["corners"]+=val
                if "shot on" in name: stats["shots_on"]+=val
                if "shot"==name: stats["shots_total"]+=val
                if "card" in name: stats["cards"]+=val
        n+=1
    if n==0:n=1
    return {
      "goals_scored_avg":stats["goals_scored"]/n,
      "goals_conceded_avg":stats["goals_conceded"]/n,
      "corners_avg":stats["corners"]/n,
      "cards_avg":stats["cards"]/n,
      "shots_total_avg":stats["shots_total"]/n,
      "shots_on_target_avg":stats["shots_on"]/n,
      "goals_scored_ht_avg":0,
      "goals_conceded_ht_avg":0,
      "corners_ht_avg":0,
      "rpg": (stats["goals_scored"]-stats["goals_conceded"])/max(n,1)
    }

def fetch_table_position(team_id:int)->int:
    return (team_id%20)+1
