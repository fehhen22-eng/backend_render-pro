import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { FileText, Upload } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { API_BASE } from "@/config";

interface ImportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface League {
  league_id: string;
  name: string;
  league_slug?: string;
  season_id?: string;
  country?: string;
}

export const ImportDialog = ({ open, onOpenChange }: ImportDialogProps) => {
  const [leagueName, setLeagueName] = useState("");
  const [country, setCountry] = useState("");
  const [leagueId, setLeagueId] = useState("");
  const [seasonId, setSeasonId] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [selectedLeagueSlug, setSelectedLeagueSlug] = useState("");
  const [availableLeagues, setAvailableLeagues] = useState<League[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    if (open) {
      fetchLeagues();
    }
  }, [open]);

  const fetchLeagues = async () => {
    try {
      const response = await fetch(`${API_BASE}/leagues`);
      const data = await response.json();
      setAvailableLeagues(data.leagues || []);
    } catch (error) {
      console.error("Erro ao buscar ligas:", error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const handleCreateLeague = async () => {
    if (!leagueName || !leagueId || !seasonId) {
      toast({
        title: "Campos obrigatórios",
        description: "Preencha todos os campos obrigatórios para criar a liga.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      const params = new URLSearchParams({ 
        league_name: leagueName,
        league_id: leagueId,
        season_id: seasonId
      });
      
      if (country) {
        params.append("country", country);
      }
      
      const response = await fetch(`${API_BASE}/create-league?${params}`, {
        method: "POST",
      });

      if (!response.ok) throw new Error("Erro ao criar liga");

      const data = await response.json();
      
      toast({
        title: "Liga criada!",
        description: `Liga "${leagueName}" criada com sucesso.`,
      });

      // Reset form
      setLeagueName("");
      setCountry("");
      setLeagueId("");
      setSeasonId("");
      onOpenChange(false);
    } catch (error) {
      toast({
        title: "Erro ao criar liga",
        description: "Não foi possível criar a liga. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleImportCSV = async () => {
    if (selectedFiles.length === 0) {
      toast({
        title: "Nenhum arquivo selecionado",
        description: "Selecione pelo menos um arquivo CSV para importar.",
        variant: "destructive",
      });
      return;
    }

    if (!selectedLeagueSlug) {
      toast({
        title: "Liga não selecionada",
        description: "Selecione uma liga existente para importar os CSVs.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    
    try {
      // Faz upload de cada CSV na liga selecionada
      let successCount = 0;
      for (const file of selectedFiles) {
        const formData = new FormData();
        const teamName = file.name.replace('.csv', '').replace(/-/g, ' ');
        
        formData.append("league", selectedLeagueSlug);
        formData.append("team_name", teamName);
        formData.append("file", file);

        const response = await fetch(`${API_BASE}/upload-csv`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          successCount++;
        }
      }

      toast({
        title: "CSVs importados!",
        description: `${successCount} de ${selectedFiles.length} arquivo(s) CSV importado(s) com sucesso na liga ${selectedLeagueSlug}.`,
      });

      // Reset
      setSelectedFiles([]);
      setSelectedLeagueSlug("");
      onOpenChange(false);
    } catch (error) {
      toast({
        title: "Erro ao importar",
        description: "Não foi possível importar os arquivos CSV.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] bg-card/95 backdrop-blur-xl border-border">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Importar Dados</DialogTitle>
          <p className="text-sm text-muted-foreground">
            Crie novas ligas ou importe times via CSV
          </p>
        </DialogHeader>

        <Tabs defaultValue="nova-liga" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-muted/50">
            <TabsTrigger value="nova-liga" className="gap-2">
              <FileText className="w-4 h-4" />
              Nova Liga
            </TabsTrigger>
            <TabsTrigger value="importar-csv" className="gap-2">
              <Upload className="w-4 h-4" />
              Importar CSV
            </TabsTrigger>
          </TabsList>

          {/* Nova Liga Tab */}
          <TabsContent value="nova-liga" className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="league-name">Nome da Liga</Label>
              <Input
                id="league-name"
                placeholder="Ex: Premier League"
                value={leagueName}
                onChange={(e) => setLeagueName(e.target.value)}
                className="bg-muted/50 border-border"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="country">País (opcional)</Label>
              <Input
                id="country"
                placeholder="Ex: Inglaterra"
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                className="bg-muted/50 border-border"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="league-id">ID da Liga</Label>
                <Input
                  id="league-id"
                  placeholder="Ex: 39"
                  value={leagueId}
                  onChange={(e) => setLeagueId(e.target.value)}
                  className="bg-muted/50 border-border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="season-id">ID da Temporada</Label>
                <Input
                  id="season-id"
                  placeholder="Ex: 2024"
                  value={seasonId}
                  onChange={(e) => setSeasonId(e.target.value)}
                  className="bg-muted/50 border-border"
                />
              </div>
            </div>

            <Button
              onClick={handleCreateLeague}
              disabled={isLoading}
              className="w-full bg-success hover:bg-success/90 text-success-foreground font-semibold h-12 mt-2"
            >
              <Upload className="w-4 h-4 mr-2" />
              {isLoading ? "Criando..." : "Criar Liga"}
            </Button>
          </TabsContent>

          {/* Importar CSV Tab */}
          <TabsContent value="importar-csv" className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="select-league">Selecionar Liga</Label>
              <Select value={selectedLeagueSlug} onValueChange={setSelectedLeagueSlug}>
                <SelectTrigger className="bg-muted/50 border-border">
                  <SelectValue placeholder="Escolha uma liga criada" />
                </SelectTrigger>
                <SelectContent>
                  {availableLeagues.length === 0 ? (
                    <SelectItem value="none" disabled>
                      Nenhuma liga disponível. Crie uma primeiro.
                    </SelectItem>
                  ) : (
                    availableLeagues.map((league) => (
                      <SelectItem key={league.league_slug || league.league_id} value={league.league_slug || league.name.toLowerCase().replace(/ /g, '-')}>
                        {league.name} {league.season_id && `(${league.season_id})`}
                      </SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Selecione a liga onde deseja importar os times
              </p>
            </div>

            <div
              className="border-2 border-dashed border-border rounded-lg p-8 text-center space-y-4 hover:border-primary/50 transition-colors cursor-pointer"
              onClick={() => document.getElementById("csv-upload")?.click()}
            >
              <div className="flex justify-center">
                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
                  <FileText className="w-8 h-8 text-primary" />
                </div>
              </div>
              <div>
                <p className="font-medium mb-1">Selecionar múltiplos arquivos CSV</p>
                <p className="text-xs text-muted-foreground">
                  Cada CSV deve conter: name, league_id, position, rpg, e outras estatísticas
                </p>
              </div>
              <input
                id="csv-upload"
                type="file"
                accept=".csv"
                multiple
                onChange={handleFileChange}
                className="hidden"
              />
            </div>

            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <Label>Arquivos selecionados ({selectedFiles.length})</Label>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {selectedFiles.map((file, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-2 rounded-md bg-muted/50 border border-border"
                    >
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm">{file.name}</span>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {(file.size / 1024).toFixed(1)} KB
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <Button
              onClick={handleImportCSV}
              disabled={selectedFiles.length === 0 || !selectedLeagueSlug || isLoading}
              className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold h-12"
            >
              <Upload className="w-4 h-4 mr-2" />
              {isLoading ? "Importando..." : "Importar Times"}
            </Button>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};
