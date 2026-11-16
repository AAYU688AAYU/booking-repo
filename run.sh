#!/bin/bash

# bookwithgulshan Traveller Booking Platform - All-in-One Startup Script

echo "=================================================="
echo "🧭 Starting bookwithgulshan Traveller Booking Platform"
echo "=================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Activate Python virtual environment and start Django backend
echo "▶ Starting Django REST Framework Backend on port 8000..."
source "$ROOT_DIR/.venv/bin/activate"
python "$ROOT_DIR/backend/manage.py migrate" > /dev/null 2>&1
python "$ROOT_DIR/backend/manage.py runserver 127.0.0.1:8000" &
DJANGO_PID=$!

# 2. Start Vite React Frontend
echo "▶ Starting Vite React Frontend on port 5173..."
cd "$ROOT_DIR/frontend"
npm run dev -- --host 127.0.0.1 &
VITE_PID=$!

echo "=================================================="
echo "✨ bookwithgulshan is Live and Ready!"
echo "🌐 Frontend URL:      http://localhost:5173/"
echo "⚙️ Backend API:       http://localhost:8000/api/"
echo "🗄️ Admin Dashboard:   http://localhost:8000/admin/"
echo "=================================================="
echo "Press Ctrl+C to stop both servers."

trap "kill $DJANGO_PID $VITE_PID; exit" INT TERM
wait
