#!/bin/bash

echo "🚀 Starting Resume Parser for Network Access"
echo "📱 Your Boss can access the app at: http://192.168.0.171:3000"
echo "🔧 Backend API will be available at: http://192.168.0.171:8000"
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ensure frontend environment is configured correctly
echo "🔧 Configuring frontend environment..."
echo "NEXT_PUBLIC_API_URL=http://192.168.0.171:8000/api" > frontend/.env.local

# Function to start backend
start_backend() {
    echo "🔧 Starting Django Backend..."
    cd backend
    source venv/bin/activate
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!
    echo "✅ Backend started with PID: $BACKEND_PID"
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Next.js Frontend..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    npm run dev &
    FRONTEND_PID=$!
    echo "✅ Frontend started with PID: $FRONTEND_PID"
    cd ..
}

# Start both services
start_backend
sleep 3
start_frontend

echo ""
echo "🎉 Both services are starting..."
echo "📱 Share this URL with your boss: http://192.168.0.171:3000"
echo "🧪 Test API directly: http://192.168.0.171:8000/api/resumes/"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait 