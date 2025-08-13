#!/bin/bash

# Setup script for Poppler environment
# Run this before starting your Django server

# Get the absolute path to the backend directory
BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POPPLER_PATH="$BACKEND_DIR/poppler-24.08.0/Library/bin"

# Add Poppler to PATH if it exists
if [ -d "$POPPLER_PATH" ]; then
    export PATH="$POPPLER_PATH:$PATH"
    echo "✓ Poppler added to PATH: $POPPLER_PATH"
    
    # Test Poppler installation
    if command -v pdfinfo >/dev/null 2>&1; then
        echo "✓ Poppler is working correctly"
        pdfinfo -v | head -1
    else
        echo "✗ Poppler installation failed"
        exit 1
    fi
else
    echo "✗ Poppler directory not found at: $POPPLER_PATH"
    echo "Please run the Poppler installation first"
    exit 1
fi

# Activate virtual environment
if [ -f "$BACKEND_DIR/venv/Scripts/activate" ]; then
    source "$BACKEND_DIR/venv/Scripts/activate"
    echo "✓ Virtual environment activated"
    echo "✓ Python version: $(python --version)"
else
    echo "✗ Virtual environment not found"
    exit 1
fi

echo ""
echo "Environment setup complete!"
echo "You can now run: python manage.py runserver"
