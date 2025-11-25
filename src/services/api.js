// URL do backend FastAPI
export const API_BASE = "https://statush2h-rkfooth2.replit.app/api";

/* ============================
   LISTAR LIGAS
============================ */
export async function getLeagues() {
  try {
    const res = await fetch(`${API_BASE}/leagues`);
    if (!res.ok) throw new Error("Erro ao buscar ligas");
    return await res.json();
  } catch (err) {
    console.error("getLeagues() error:", err);
    return [];
  }
}

/* ============================
   LISTAR TIMES DA LIGA
============================ */
export async function getTeams(leagueId) {
  try {
    const res = await fetch(`${API_BASE}/teams/${leagueId}`);
    if (!res.ok) throw new Error("Erro ao buscar times");
    return await res.json();
  } catch (err) {
    console.error("getTeams() error:", err);
    return [];
  }
}

/* ============================
   ANÁLISE H2H
============================ */
export async function analyzeH2H(payload) {
  try {
    const res = await fetch(`${API_BASE}/h2h`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Erro ao analisar confronto");

    return await res.json();
  } catch (err) {
    console.error("analyzeH2H() error:", err);
    return null;
  }
}
