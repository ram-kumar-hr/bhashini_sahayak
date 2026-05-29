#!/usr/bin/env bash
# start.sh — Launch all Bhashini Sahayak services
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

log()  { echo -e "${GREEN}[Sahayak]${NC} $*"; }
warn() { echo -e "${YELLOW}[Sahayak]${NC} $*"; }
err()  { echo -e "${RED}[Sahayak]${NC} $*"; }

# ── 1. Check .env ─────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
  warn ".env not found — copying from .env.example"
  cp .env.example .env
  err "Please edit .env and add your OPENAI_API_KEY, then re-run this script."
  exit 1
fi

# ── 2. Start Qdrant ───────────────────────────────────────────────────────────
log "Starting Qdrant via Docker Compose…"
docker compose up -d qdrant
log "Waiting for Qdrant to be ready…"
for i in $(seq 1 15); do
  if curl -sf http://localhost:6333/healthz > /dev/null 2>&1; then
    log "Qdrant is ready."
    break
  fi
  sleep 2
done

# ── 3. Python venv ────────────────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
  log "Creating Python virtual environment…"
  python3 -m venv .venv
fi
source .venv/bin/activate

log "Installing Python dependencies…"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# ── 4. Ingest SOPs (only if collection is empty) ──────────────────────────────
log "Ingesting SOP documents into Qdrant…"
python -m scripts.ingest_sop || warn "SOP ingest failed (check OPENAI_API_KEY). Continuing anyway."

# ── 5. Start FastAPI backend ──────────────────────────────────────────────────
log "Starting FastAPI backend on http://localhost:8000 …"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
log "Backend PID: $BACKEND_PID"

# ── 6. Start React frontend ───────────────────────────────────────────────────
cd frontend
if [ ! -d "node_modules" ]; then
  log "Installing Node dependencies…"
  npm install
fi
log "Starting React dev server on http://localhost:5173 …"
npm run dev &
FRONTEND_PID=$!
cd ..

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "  Bhashini Sahayak is running!"
log "  Frontend : http://localhost:5173"
log "  Backend  : http://localhost:8000"
log "  API Docs : http://localhost:8000/docs"
log "  Qdrant   : http://localhost:6333/dashboard"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "Press Ctrl+C to stop all services."

# Wait and clean up on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker compose stop qdrant" EXIT
wait
