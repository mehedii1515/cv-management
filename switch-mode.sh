#!/bin/bash

MODE=$1

if [ "$MODE" = "local" ]; then
    echo "Switching to local development mode..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > frontend/.env.local
    echo "Starting servers in local mode..."
    echo "Backend will be available at: http://localhost:8000"
    echo "Frontend will be available at: http://localhost:3000"
    
    # Start the backend server
    cd backend
    source venv/Scripts/activate
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!

    # Start the frontend server in dev mode
    cd ../frontend
    npm run dev -- -H 0.0.0.0 &
    FRONTEND_PID=$!

elif [ "$MODE" = "network" ]; then
    echo "Switching to network mode..."
    echo "NEXT_PUBLIC_API_URL=http://192.168.1.152:8000/api" > frontend/.env.local
    echo "Starting servers in network mode..."
    echo "Backend will be available at: http://192.168.1.152:8000"
    echo "Frontend will be available at: http://192.168.1.152:3000"
    
    # Start the backend server
    cd backend
    source venv/Scripts/activate
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!

    # Build and start the frontend server in production mode
    cd ../frontend
    npm run dev
    npm run start -- -H 0.0.0.0 &
    FRONTEND_PID=$!

else
    echo "Please specify mode: local or network"
    echo "Usage: ./switch-mode.sh local|network"
    exit 1
fi

echo "Press Ctrl+C to stop both servers"
wait $BACKEND_PID $FRONTEND_PID 