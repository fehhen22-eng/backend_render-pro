# Backend H2H Predictor – Pacote Final

Gerado em: 2025-11-23T01:59:57.040580 UTC

## Estrutura

- `main.py` – ponto de entrada FastAPI
- `routers/`
  - `leagues.py` – lista/cria ligas em `data/leagues`
  - `teams.py` – lista times (1 CSV por time)
  - `h2h.py` – endpoint de análise H2H
  - `upload.py` – upload de CSV por time
  - `update.py` – rotas de atualização (`/api/update/all` e `/api/update/league/{league_id}`)
- `updater/`
  - `sofascorer.py` – integração SIMULADA com SofaScore (pronto para ser trocado por API real)
  - `update_engine.py` – motor de atualização incremental dos CSVs
- `requirements.txt` – dependências do backend

## Como rodar (local, Replit ou Render)

1. Instale as dependências:

   ```bash
   pip install -r backend/requirements.txt
   ```

2. Inicie o servidor FastAPI com Uvicorn (a partir da raiz do projeto):

   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

   No Render, use o comando:

   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

3. Garanta que os CSVs estão em:

   ```
   data/leagues/{league_id}/{time}.csv
   ```

4. Use:

   - `GET /api/leagues`
   - `GET /api/league/{league_id}/teams`
   - `GET /api/h2h?league=...&home=...&away=...`
   - `POST /api/upload-csv`
   - `GET /api/update/all`
   - `GET /api/update/league/{league_id}`

## Importante

- O módulo `updater/sofascorer.py` está com valores **SIMULADOS**.
  Ele foi desenhado para ser facilmente substituído por integração real
  com SofaScore (ou outra fonte), inclusive pela IA do Replit.
- O motor `update_engine.py` **não apaga colunas existentes** nos CSVs:
  apenas atualiza/insere:
    - `team_id`, `team_name`, `table_position`, `last_update_utc`
    - métricas médias de gols, escanteios, cartões, chutes e RPG.

Depois que a integração real com SofaScore for implementada,
o painel H2H poderá trabalhar 100% com dados atualizados automaticamente.
