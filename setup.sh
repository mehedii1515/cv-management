#!/bin/bash

echo "========================================"
echo "Resume Parser - Automatic Setup (Linux/Mac)"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.10, 3.11, or 3.12"
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"

# Check Python version compatibility
python3 -c "import sys; exit(0 if (3,10) <= sys.version_info[:2] <= (3,12) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Python version $PYTHON_VERSION is not supported${NC}"
    echo "Please install Python 3.10, 3.11, or 3.12"
    echo "The unstructured library requires Python 3.10-3.12"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION is compatible${NC}"

# Create virtual environment
echo
echo "Creating virtual environment..."
if [ -d "backend/venv" ]; then
    echo "Virtual environment already exists, removing old one..."
    rm -rf backend/venv
fi

cd backend
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment and install dependencies
echo
echo "Installing Python dependencies..."
source venv/bin/activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to install Python dependencies${NC}"
    echo "Please check your internet connection and try again"
    exit 1
fi
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Download and setup Poppler
echo
echo "Setting up Poppler for PDF processing..."
if [ ! -d "poppler-24.08.0" ]; then
    echo "Downloading Poppler..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - install via package manager
        if command -v apt-get &> /dev/null; then
            echo "Installing Poppler via apt..."
            sudo apt-get update && sudo apt-get install -y poppler-utils
        elif command -v yum &> /dev/null; then
            echo "Installing Poppler via yum..."
            sudo yum install -y poppler-utils
        elif command -v pacman &> /dev/null; then
            echo "Installing Poppler via pacman..."
            sudo pacman -S poppler
        else
            echo -e "${YELLOW}WARNING: Could not install Poppler automatically${NC}"
            echo "Please install poppler-utils using your package manager"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "Installing Poppler via Homebrew..."
            brew install poppler
        else
            echo -e "${YELLOW}WARNING: Homebrew not found${NC}"
            echo "Please install Homebrew or install Poppler manually"
        fi
    fi
    echo -e "${GREEN}✓ Poppler setup attempted${NC}"
else
    echo -e "${GREEN}✓ Poppler already installed${NC}"
fi

# Setup environment file
echo
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Environment file created (.env)${NC}"
    echo
    echo -e "${YELLOW}IMPORTANT: Please edit the .env file and add your API keys:${NC}"
    echo "- OPENAI_API_KEY=your_openai_key_here"
    echo "- GOOGLE_API_KEY=your_gemini_key_here"
    echo
else
    echo -e "${GREEN}✓ Environment file already exists${NC}"
fi

# Run initial Django setup
echo
echo "Setting up Django database..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to setup database${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Database setup complete${NC}"

# Create superuser prompt
echo
echo "Creating Django admin user..."
read -p "Do you want to create an admin user now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Install frontend dependencies
echo
echo "Setting up frontend..."
cd ../frontend

if [ -d "node_modules" ]; then
    echo "Node modules already exist, skipping npm install"
else
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo -e "${YELLOW}WARNING: npm is not installed${NC}"
        echo "Please install Node.js from https://nodejs.org"
        echo "Frontend setup skipped"
    else
        echo "Installing frontend dependencies..."
        npm install
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: Failed to install frontend dependencies${NC}"
            echo "Please check your Node.js installation"
        else
            echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
        fi
    fi
fi

cd ../backend

echo
echo "========================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================"
echo
echo "To start the application:"
echo "1. Edit .env file with your API keys"
echo "2. Run: ./start_servers.sh"
echo
echo "For manual startup:"
echo "Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "Frontend: cd frontend && npm run dev"
echo
echo "Admin panel: http://localhost:8000/admin/"
echo "Application: http://localhost:3000/"
echo
