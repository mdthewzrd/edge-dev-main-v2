#!/bin/bash

echo "🚀 Starting Edge-Dev-Main Development Environment..."

# Start Backend
echo "⚡ Starting FastAPI Backend..."
cd backend
python main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Next.js Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ All services started!"
echo "  Frontend: http://localhost:5665"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
