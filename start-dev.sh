#!/bin/bash
set -e

echo "🚀 Starte Backend..."
cd backend

# check for uv installation, else use pip venv
if command -v uv &> /dev/null
then
    echo "Starting backend with uv..."
    uv run uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
else
    echo "Using standard Python venv & pip..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
fi

cd ../frontend

echo "🚀 Starte Frontend (Nuxt)..."
if [ ! -d "node_modules" ]; then
    echo "📦 Installiere Frontend-Abhängigkeiten..."
    npm install --silent --no-audit --no-fund #--loglevel error
fi

npm run dev -- --port 3000 &

FRONTEND_PID=$!

echo "---------------------------------------------------"
echo "✅ Backend:  http://localhost:8000"
echo "✅ Frontend: http://localhost:3000"
echo "---------------------------------------------------"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait