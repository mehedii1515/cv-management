#!/bin/bash

echo "========================================"
echo "Resume Parser - Stopping Servers"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local service_name=$2
    
    pids=$(lsof -ti:$port)
    if [ ! -z "$pids" ]; then
        echo "Stopping $service_name (port $port)..."
        kill $pids
        sleep 2
        
        # Force kill if still running
        pids=$(lsof -ti:$port)
        if [ ! -z "$pids" ]; then
            echo "Force stopping $service_name..."
            kill -9 $pids
        fi
        echo -e "${GREEN}✓ $service_name stopped${NC}"
    else
        echo "$service_name is not running on port $port"
    fi
}

# Stop Django server (port 8000)
kill_port 8000 "Backend server"

# Stop Next.js server (port 3000)
kill_port 3000 "Frontend server"

# Also kill any python manage.py runserver processes
pkill -f "python manage.py runserver"

# Kill any npm run dev processes
pkill -f "npm run dev"

echo
echo -e "${GREEN}All servers stopped${NC}"
echo
