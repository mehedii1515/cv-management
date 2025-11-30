#!/bin/bash

# LibreOffice Installation Script for DOCX to PDF Conversion
# This script installs LibreOffice for headless document conversion

echo "Setting up LibreOffice for document conversion..."

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux system"
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        echo "Installing LibreOffice on Ubuntu/Debian..."
        sudo apt-get update
        sudo apt-get install -y libreoffice --no-install-recommends
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        echo "Installing LibreOffice on CentOS/RHEL..."
        sudo yum install -y libreoffice-headless
    elif command -v dnf &> /dev/null; then
        # Fedora
        echo "Installing LibreOffice on Fedora..."
        sudo dnf install -y libreoffice-headless
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS system"
    if command -v brew &> /dev/null; then
        echo "Installing LibreOffice via Homebrew..."
        brew install --cask libreoffice
    else
        echo "Homebrew not found. Please install Homebrew first or download LibreOffice manually from https://www.libreoffice.org/download/download/"
        exit 1
    fi
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OS" == "Windows_NT" ]]; then
    # Windows
    echo "Detected Windows system"
    echo "Please download and install LibreOffice manually from:"
    echo "https://www.libreoffice.org/download/download/"
    echo ""
    echo "Alternative: Use Chocolatey package manager:"
    echo "choco install libreoffice"
    echo ""
    echo "After installation, make sure 'libreoffice' command is available in PATH"
else
    echo "Unknown operating system: $OSTYPE"
    echo "Please install LibreOffice manually from https://www.libreoffice.org/download/download/"
    exit 1
fi

# Test LibreOffice installation
echo "Testing LibreOffice installation..."
if command -v libreoffice &> /dev/null; then
    echo "✅ LibreOffice installed successfully!"
    libreoffice --version
    echo ""
    echo "🚀 Your system is ready for DOCX to PDF conversion!"
else
    echo "❌ LibreOffice installation failed or not found in PATH"
    echo "Please ensure LibreOffice is installed and the 'libreoffice' command is available"
    exit 1
fi
