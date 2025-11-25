import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Trophy, TrendingUp, Target, AlertCircle, Lightbulb } from "lucide-react";
import { StatBar } from "./StatBar";

interface AsianMarketSuggestion {
  line: string;
  reason: string;
  explanation: string;
}

interface AsianMarket {
  market_name: string;
  suggestions: {
    ousada: AsianMarketSuggestion;
    conservadora: AsianMarketSuggestion;
  };
}

interface AnalysisResultsProps {
  homeTeam: string;
  awayTeam: string;
  onBack: () => void;
  asianMarkets?: AsianMarket[];
}

export const AnalysisResults = ({ homeTeam, awayTeam, onBack, asianMarkets = [] }: AnalysisResultsProps) => {
  const formRecent = [
    { result: "V", color: "success" },
    { result: "V", color: "success" },
    { result: "E", color: "warning" },
    { result: "V", color: "success" },
    { result: "V", color: "success" },
  ];

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Button onClick={onBack} variant="ghost" className="gap-2">
        <ArrowLeft className="w-4 h-4" />
        Voltar
      </Button>

      {/* Team Comparison Header */}
      <div className="grid grid-cols-2 gap-4">
        {/* Home Team */}
        <Card className="glass-card border-success/30 p-6">
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="w-20 h-20 rounded-full bg-success/20 flex items-center justify-center ring-2 ring-success/30">
              <Trophy className="w-10 h-10 text-success" />
            </div>
            <div>
              <h3 className="text-xl font-bold">{homeTeam}</h3>
              <Badge className="bg-success/20 text-success border-success/30 mt-2">Mandante</Badge>
            </div>
            <div className="w-full space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Posição</span>
                <span className="font-semibold text-success">2º</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Força (RPG)</span>
                <span className="font-semibold text-success">2.38</span>
              </div>
              <div className="space-y-2">
                <span className="text-xs text-muted-foreground">Forma Recente</span>
                <div className="flex gap-1 justify-center">
                  {formRecent.map((form, idx) => (
                    <div
                      key={idx}
                      className={`w-8 h-8 rounded-md flex items-center justify-center font-bold text-xs ${
                        form.color === "success"
                          ? "bg-success/20 text-success"
                          : "bg-warning/20 text-warning"
                      }`}
                    >
                      {form.result}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Away Team */}
        <Card className="glass-card border-info/30 p-6">
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="w-20 h-20 rounded-full bg-info/20 flex items-center justify-center ring-2 ring-info/30">
              <Trophy className="w-10 h-10 text-info" />
            </div>
            <div>
              <h3 className="text-xl font-bold">{awayTeam}</h3>
              <Badge className="bg-info/20 text-info border-info/30 mt-2">Visitante</Badge>
            </div>
            <div className="w-full space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Posição</span>
                <span className="font-semibold text-info">1º</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Força (RPG)</span>
                <span className="font-semibold text-info">2.45</span>
              </div>
              <div className="space-y-2">
                <span className="text-xs text-muted-foreground">Forma Recente</span>
                <div className="flex gap-1 justify-center">
                  {formRecent.map((form, idx) => (
                    <div
                      key={idx}
                      className={`w-8 h-8 rounded-md flex items-center justify-center font-bold text-xs ${
                        form.color === "success"
                          ? "bg-success/20 text-success"
                          : "bg-warning/20 text-warning"
                      }`}
                    >
                      {form.result}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Prediction */}
      <Card className="glass-card border-accent/30 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
            <Target className="w-5 h-5 text-accent" />
          </div>
          <div>
            <h3 className="font-bold">Previsão</h3>
            <p className="text-xs text-muted-foreground">Placar mais provável</p>
          </div>
        </div>
        <div className="flex items-center justify-center gap-4 py-6">
          <span className="text-5xl font-bold text-success">3</span>
          <span className="text-3xl text-muted-foreground">×</span>
          <span className="text-5xl font-bold text-info">2</span>
        </div>
      </Card>

      {/* Probabilities */}
      <Card className="glass-card border-primary/30 p-6">
        <div className="flex items-center gap-3 mb-6">
          <TrendingUp className="w-5 h-5 text-primary" />
          <h3 className="font-bold">Probabilidades</h3>
        </div>
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 rounded-lg bg-success/10 border border-success/20">
            <div className="text-3xl font-bold text-success mb-1">43%</div>
            <div className="text-xs text-muted-foreground">Vitória Casa</div>
          </div>
          <div className="text-center p-4 rounded-lg bg-muted/30 border border-border">
            <div className="text-3xl font-bold text-muted-foreground mb-1">23%</div>
            <div className="text-xs text-muted-foreground">Empate</div>
          </div>
          <div className="text-center p-4 rounded-lg bg-info/10 border border-info/20">
            <div className="text-3xl font-bold text-info mb-1">34%</div>
            <div className="text-xs text-muted-foreground">Vitória Fora</div>
          </div>
        </div>
        <div className="space-y-3">
          <StatBar label="X1 (Empate ou Casa)" value={66} color="success" />
          <StatBar label="Over 1.5" value={87} color="info" />
          <StatBar label="Over 2.5" value={73} color="warning" />
          <StatBar label="BTTS" value={50} color="destructive" />
        </div>
      </Card>

      {/* Asian Markets Recommendations */}
      {asianMarkets && asianMarkets.length > 0 && (
        <Card className="glass-card border-gradient-to-r from-accent/30 to-primary/30 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent to-primary flex items-center justify-center">
              <Target className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold">Mercados Asiáticos Recomendados</h3>
              <p className="text-xs text-muted-foreground">2 melhores mercados para esta partida</p>
            </div>
          </div>

          {/* Render each Asian Market */}
          <div className="space-y-6">
            {asianMarkets.map((market, index) => (
              <div key={index} className="space-y-4">
                <h3 className="font-bold text-lg text-primary border-b border-primary/20 pb-2">
                  {market.market_name}
                </h3>
                
                {/* Ousada Suggestion */}
                <div className="p-4 rounded-lg bg-gradient-to-r from-purple-500/10 to-purple-600/10 border-2 border-purple-500/30">
                  <div className="flex items-start gap-3">
                    <Badge className="bg-purple-500 text-white border-0 mt-1">🟣 Ousada</Badge>
                    <div className="flex-1">
                      <h4 className="font-bold text-lg mb-2">{market.suggestions.ousada.line}</h4>
                      <p className="text-sm text-muted-foreground mb-3">
                        <span className="font-semibold">Motivo:</span> {market.suggestions.ousada.reason}
                      </p>
                      <div className="p-3 rounded-md bg-background/50 border border-border">
                        <p className="text-xs font-medium mb-1">Como funciona:</p>
                        <p className="text-xs text-muted-foreground">
                          {market.suggestions.ousada.explanation}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Conservadora Suggestion */}
                <div className="p-4 rounded-lg bg-gradient-to-r from-green-500/10 to-green-600/10 border-2 border-green-500/30">
                  <div className="flex items-start gap-3">
                    <Badge className="bg-green-500 text-white border-0 mt-1">🟢 Conservadora</Badge>
                    <div className="flex-1">
                      <h4 className="font-bold text-lg mb-2">{market.suggestions.conservadora.line}</h4>
                      <p className="text-sm text-muted-foreground mb-3">
                        <span className="font-semibold">Motivo:</span> {market.suggestions.conservadora.reason}
                      </p>
                      <div className="p-3 rounded-md bg-background/50 border border-border">
                        <p className="text-xs font-medium mb-1">Como funciona:</p>
                        <p className="text-xs text-muted-foreground">
                          {market.suggestions.conservadora.explanation}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* AI Analysis */}
      <Card className="glass-card border-accent/30 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
            <Lightbulb className="w-5 h-5 text-accent" />
          </div>
          <h3 className="font-bold">Análise Inteligente</h3>
        </div>
        <div className="space-y-3 text-sm text-muted-foreground leading-relaxed">
          <p>
            1. O {homeTeam} é o favorito com 43%, justificado pelo fator casa e uma média de 2.6 gols marcados em casa, apesar da ligeira vantagem do {awayTeam} em RPG (2.45).
          </p>
          <p>
            2. Um possível placar é {homeTeam} 3 x 2 {awayTeam}, dada a tendência de ambos os times marcarem muitos gols, reforçada pelo over 2.5 em 73% para o {homeTeam}.
          </p>
          <p>
            3. A melhor aposta seria "{homeTeam} vence" com odd estimada em 2.30, considerando a probabilidade de vitória e o fator casa.
          </p>
        </div>
      </Card>

      {/* Alerts */}
      <Card className="glass-card border-destructive/30 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-destructive/20 flex items-center justify-center">
            <AlertCircle className="w-5 h-5 text-destructive" />
          </div>
          <div>
            <h3 className="font-bold">Alertas (4)</h3>
            <p className="text-xs text-muted-foreground">Fatores importantes</p>
          </div>
        </div>
        <div className="space-y-2">
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm">
            {homeTeam} marca HT (85%)
          </div>
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm">
            Alta chance 1.5 escanteio HT time casa
          </div>
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm">
            Over 2.5 FT forte
          </div>
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm">
            Over 9.5 cantos (13.3)
          </div>
        </div>
      </Card>

      {/* Goal Statistics */}
      <Card className="glass-card border-primary/30 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
            <Target className="w-5 h-5 text-primary" />
          </div>
          <h3 className="font-bold">Estatísticas de Gols</h3>
        </div>
        <div className="space-y-6">
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Média de Gols Marcados FT</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={2.60} max={3} color="success" showValue />
              <StatBar label={awayTeam} value={2.30} max={3} color="info" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Média de Gols Sofridos FT</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={1.00} max={2} color="success" showValue />
              <StatBar label={awayTeam} value={1.10} max={2} color="info" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Over/Under</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 0.5 HT" value={82} color="success" />
                <StatBar label="" value={75} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 1.5 HT" value={60} color="success" />
                <StatBar label="" value={55} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 1.5 FT" value={88} color="success" />
                <StatBar label="" value={85} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 2.5 FT" value={75} color="success" />
                <StatBar label="" value={70} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 3.5 FT" value={50} color="success" />
                <StatBar label="" value={48} color="info" />
              </div>
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">BTTS e Frequências</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="BTTS (%)" value={48} color="success" />
                <StatBar label="" value={52} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Frequência Marcar HT" value={85} color="success" />
                <StatBar label="" value={78} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Frequência Sofrer HT" value={38} color="warning" />
                <StatBar label="" value={42} color="warning" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Frequência Marcar FT" value={92} color="success" />
                <StatBar label="" value={90} color="info" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Frequência Sofrer FT" value={60} color="warning" />
                <StatBar label="" value={65} color="warning" />
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Corners Statistics */}
      <Card className="glass-card border-warning/30 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-warning" />
            </div>
            <h3 className="font-bold">Estatísticas de Escanteios</h3>
          </div>
          <Badge className="bg-warning/20 text-warning border-warning/30">Forte</Badge>
        </div>
        <div className="space-y-6">
          <div className="p-4 rounded-lg bg-gradient-to-r from-warning/20 to-warning/10 border border-warning/30">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Projeção Combinada</span>
              <span className="text-2xl font-bold text-warning">13.3 cantos</span>
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Cantos Médios HT</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={3.30} max={5} color="warning" showValue />
              <StatBar label={awayTeam} value={3.00} max={5} color="warning" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Cantos Médios FT</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={6.80} max={10} color="warning" showValue />
              <StatBar label={awayTeam} value={6.50} max={10} color="warning" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Over Cantos</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 5.5" value={78} color="warning" />
                <StatBar label="" value={75} color="warning" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 7.5" value={62} color="warning" />
                <StatBar label="" value={58} color="warning" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 8.5" value={42} color="warning" />
                <StatBar label="" value={38} color="warning" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 9.5" value={28} color="warning" />
                <StatBar label="" value={25} color="warning" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 10.5" value={15} color="warning" />
                <StatBar label="" value={12} color="warning" />
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Shots & Finishing */}
      <Card className="glass-card border-destructive/30 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-destructive/20 flex items-center justify-center">
            <Target className="w-5 h-5 text-destructive" />
          </div>
          <h3 className="font-bold">Chutes e Finalizações</h3>
        </div>
        <div className="space-y-6">
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Chutes Totais por Jogo</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={17.80} max={20} color="destructive" showValue />
              <StatBar label={awayTeam} value={16.20} max={20} color="destructive" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Chutes no Gol</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={6.90} max={10} color="destructive" showValue />
              <StatBar label={awayTeam} value={6.50} max={10} color="destructive" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Finalizações Perigosas</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={58.00} max={100} color="destructive" showValue />
              <StatBar label={awayTeam} value={55.00} max={100} color="destructive" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Ataques</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={138.00} max={150} color="destructive" showValue />
              <StatBar label={awayTeam} value={128.00} max={150} color="destructive" showValue />
            </div>
          </div>
        </div>
      </Card>

      {/* Cards Statistics */}
      <Card className="glass-card border-chart-red/30 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-chart-red/20 flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-chart-red" />
            </div>
            <h3 className="font-bold">Estatísticas de Cartões</h3>
          </div>
          <Badge className="bg-success/20 text-success border-success/30">Poucos Cartões</Badge>
        </div>
        <div className="space-y-6">
          <div className="p-4 rounded-lg bg-gradient-to-r from-success/20 to-success/10 border border-success/30">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Projeção Combinada</span>
              <span className="text-2xl font-bold text-success">0.0 cartões</span>
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Cartões Médios</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={0} max={5} color="success" showValue />
              <StatBar label={awayTeam} value={0} max={5} color="info" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Cartões Amarelos</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={0} max={5} color="warning" showValue />
              <StatBar label={awayTeam} value={0} max={5} color="warning" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Cartões Vermelhos</h4>
            <div className="grid grid-cols-2 gap-4">
              <StatBar label={homeTeam} value={0} max={1} color="destructive" showValue />
              <StatBar label={awayTeam} value={0} max={1} color="destructive" showValue />
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium mb-3 text-muted-foreground">Over Cartões</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 2.5" value={0} color="muted" />
                <StatBar label="" value={0} color="muted" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 3.5" value={0} color="muted" />
                <StatBar label="" value={0} color="muted" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <StatBar label="Over 4.5" value={0} color="muted" />
                <StatBar label="" value={0} color="muted" />
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
