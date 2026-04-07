#!/bin/bash

# ArcReel Development Environment
echo "=========================================="
echo "  ArcReel: Starting AI Video Workspace"
echo "=========================================="
echo ""

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM EXIT

# 1. Backend Service
echo "[1/2] Starting Backend on port 1241..."
if command -v uv >/dev/null 2>&1; then
    uv run python -m uvicorn server.app:app --port 1241 --reload &
else
    echo "Warning: 'uv' not found, trying to run with python3 directly..."
    # Attempt to use venv if it exists
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        python -m uvicorn server.app:app --port 1241 --reload &
    else
        python3 -m uvicorn server.app:app --port 1241 --reload &
    fi
fi
BACKEND_PID=$!

# 2. Frontend Service
echo "[2/2] Starting Frontend on port 5173..."
cd frontend || exit
if command -v pnpm >/dev/null 2>&1; then
    pnpm run dev &
else
    echo "Warning: 'pnpm' not found, trying to run with npm..."
    npm run dev &
fi
FRONTEND_PID=$!

cd ..

echo ""
echo "=========================================="
echo "  All services are launching!"
echo "  - Backend: http://localhost:1241"
echo "  - Frontend: http://localhost:5173"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all services."

# Wait for background processes
wait
