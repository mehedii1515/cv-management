#!/bin/bash

echo "========================================"
echo "Resume Parser - Starting Servers"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    echo "Please run setup.sh first"
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}ERROR: .env file not found${NC}"
    echo "Please copy backend/.env.example to backend/.env and add your API keys"
    exit 1
fi

# Check ports
if check_port 8000; then
    echo -e "${YELLOW}WARNING: Port 8000 is already in use${NC}"
    echo "Another Django server might be running"
fi

if check_port 3000; then
    echo -e "${YELLOW}WARNING: Port 3000 is already in use${NC}"
    echo "Another Next.js server might be running"
fi

echo "Starting backend server..."
cd backend
source venv/bin/activate

# Start Django in background
nohup python manage.py runserver 8000 > server.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"

cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}WARNING: Frontend dependencies not installed${NC}"
    echo "Run: cd frontend && npm install"
else
    echo "Starting frontend server..."
    # Start Next.js in background
    nohup npm run dev > ../backend/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend server started (PID: $FRONTEND_PID)${NC}"
fi

echo
echo "========================================"
echo -e "${GREEN}Servers Started!${NC}"
echo "========================================"
echo
echo "Backend:  http://localhost:8000/"
echo "Frontend: http://localhost:3000/"
echo "Admin:    http://localhost:8000/admin/"
echo
echo "Logs:"
echo "Backend:  tail -f backend/server.log"
echo "Frontend: tail -f backend/frontend.log"
echo
echo "To stop servers: ./stop_servers.sh"
echo
