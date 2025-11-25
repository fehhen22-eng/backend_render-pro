import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { ChevronDown, TrendingUp, Layers, Upload, Search } from "lucide-react";
import { AnalysisResults } from "@/components/AnalysisResults";
import { ImportDialog } from "@/components/ImportDialog";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE } from "@/config";

interface League {
  league_id: string;
  name: string;
  league_slug?: string;
  season_id?: string;
}

interface Team {
  team: string;
  display_name: string;
  team_id?: string | null;
}

const Index = () => {
  const [showResults, setShowResults] = useState(false);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [leagues, setLeagues] = useState<League[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [league, setLeague] = useState("");
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchLeagues();
  }, []);

  useEffect(() => {
    if (league) {
      fetchTeams(league);
    }
  }, [league]);

  const fetchLeagues = async () => {
    try {
      const response = await fetch(`${API_BASE}/leagues`);
      const data = await response.json();
      setLeagues(data.leagues || []);
      if (data.leagues && data.leagues.length > 0) {
        setLeague(data.leagues[0].league_slug || data.leagues[0].name.toLowerCase().replace(/ /g, '-'));
      }
    } catch (error) {
      console.error("Erro ao buscar ligas:", error);
    }
  };

  const fetchTeams = async (leagueSlug: string) => {
    try {
      const response = await fetch(`${API_BASE}/league/${leagueSlug}/teams`);
      const data = await response.json();
      setTeams(data.teams || []);
      setHomeTeam("");
      setAwayTeam("");
    } catch (error) {
      console.error("Erro ao buscar times:", error);
    }
  };

  const handleAnalyze = async () => {
    if (league && homeTeam && awayTeam) {
      setIsLoading(true);
      try {
        const response = await fetch(
          `/api/h2h?league=${encodeURIComponent(league)}&home=${encodeURIComponent(homeTeam)}&away=${encodeURIComponent(awayTeam)}`
        );
        
        if (!response.ok) {
          throw new Error("Erro ao buscar análise");
        }
        
        const data = await response.json();
        setAnalysisData(data);
        setShowResults(true);
      } catch (error) {
        toast({
          title: "Erro",
          description: "Não foi possível carregar a análise. Verifique se os times existem.",
          variant: "destructive",
        });
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl md:text-4xl font-bold text-center gradient-text">
            H2H Predictor
          </h1>
          <p className="text-center text-muted-foreground mt-2">
            Análise completa de confrontos com estatísticas avançadas e IA
          </p>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 space-y-6">
        {/* Palpites do Dia - Collapsible */}
        <Collapsible>
          <Card className="glass-card border-warning/20">
            <CollapsibleTrigger className="w-full">
              <div className="flex items-center justify-between p-4 hover:bg-muted/10 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-warning" />
                  </div>
                  <span className="text-lg font-semibold">Palpites do Dia</span>
                </div>
                <ChevronDown className="w-5 h-5 text-muted-foreground" />
              </div>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className="px-4 pb-4 space-y-3">
                <p className="text-sm text-muted-foreground">
                  Nenhum palpite disponível no momento.
                </p>
              </div>
            </CollapsibleContent>
          </Card>
        </Collapsible>

        {/* Apostas Múltiplas - Collapsible */}
        <Collapsible>
          <Card className="glass-card border-info/20">
            <CollapsibleTrigger className="w-full">
              <div className="flex items-center justify-between p-4 hover:bg-muted/10 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-info/20 flex items-center justify-center">
                    <Layers className="w-5 h-5 text-info" />
                  </div>
                  <span className="text-lg font-semibold">Apostas Múltiplas</span>
                </div>
                <ChevronDown className="w-5 h-5 text-muted-foreground" />
              </div>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className="px-4 pb-4 space-y-3">
                <p className="text-sm text-muted-foreground">
                  Nenhuma aposta múltipla configurada.
                </p>
              </div>
            </CollapsibleContent>
          </Card>
        </Collapsible>

        {/* Análise de Confronto */}
        {!showResults && (
          <Card className="glass-card border-success/20">
            <div className="p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-success/20 flex items-center justify-center">
                    <Search className="w-6 h-6 text-success" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold">Análise de Confronto</h2>
                    <p className="text-sm text-muted-foreground">
                      Selecione os times para análise H2H
                    </p>
                  </div>
                </div>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="gap-2"
                  onClick={() => setShowImportDialog(true)}
                >
                  <Upload className="w-4 h-4" />
                  Importar Liga/CSV
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-muted-foreground">Liga</label>
                  <Select value={league} onValueChange={setLeague}>
                    <SelectTrigger className="bg-muted/50 border-border">
                      <SelectValue placeholder="Selecionar liga" />
                    </SelectTrigger>
                    <SelectContent>
                      {leagues.length === 0 ? (
                        <SelectItem value="none" disabled>
                          Nenhuma liga disponível
                        </SelectItem>
                      ) : (
                        leagues.map((l) => (
                          <SelectItem key={l.league_slug || l.league_id} value={l.league_slug || l.name.toLowerCase().replace(/ /g, '-')}>
                            {l.name} {l.season_id && `(${l.season_id})`}
                          </SelectItem>
                        ))
                      )}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-muted-foreground">Time Mandante</label>
                  <Select value={homeTeam} onValueChange={setHomeTeam} disabled={!league || teams.length === 0}>
                    <SelectTrigger className="bg-muted/50 border-border">
                      <SelectValue placeholder="Selecionar mandante" />
                    </SelectTrigger>
                    <SelectContent>
                      {teams.length === 0 ? (
                        <SelectItem value="none" disabled>
                          Selecione uma liga primeiro
                        </SelectItem>
                      ) : (
                        teams.map((team) => (
                          <SelectItem key={team.team} value={team.team}>
                            {team.display_name}
                          </SelectItem>
                        ))
                      )}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-muted-foreground">Time Visitante</label>
                  <Select value={awayTeam} onValueChange={setAwayTeam} disabled={!league || teams.length === 0}>
                    <SelectTrigger className="bg-muted/50 border-border">
                      <SelectValue placeholder="Selecionar visitante" />
                    </SelectTrigger>
                    <SelectContent>
                      {teams.length === 0 ? (
                        <SelectItem value="none" disabled>
                          Selecione uma liga primeiro
                        </SelectItem>
                      ) : (
                        teams.map((team) => (
                          <SelectItem key={team.team} value={team.team}>
                            {team.display_name}
                          </SelectItem>
                        ))
                      )}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button
                onClick={handleAnalyze}
                disabled={!league || !homeTeam || !awayTeam || isLoading}
                className="w-full bg-success hover:bg-success/90 text-success-foreground font-semibold h-12"
              >
                <Search className="w-5 h-5 mr-2" />
                {isLoading ? "Analisando..." : "Analisar Confronto"}
              </Button>
            </div>
          </Card>
        )}

        {/* Results */}
        {showResults && analysisData && (
          <AnalysisResults
            homeTeam={homeTeam}
            awayTeam={awayTeam}
            onBack={() => setShowResults(false)}
            asianMarkets={analysisData.asian_markets}
          />
        )}
      </div>

      {/* Import Dialog */}
      <ImportDialog 
        open={showImportDialog} 
        onOpenChange={(open) => {
          setShowImportDialog(open);
          if (!open) {
            fetchLeagues();
          }
        }} 
      />
    </div>
  );
};

export default Index;
