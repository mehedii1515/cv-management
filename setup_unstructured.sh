#!/bin/bash

# Resume Parser - Unstructured Setup Script
# This script installs the required dependencies for Unstructured document processing

echo "🚀 Setting up Resume Parser with Unstructured..."
echo "================================================"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  WARNING: You are not in a virtual environment!"
    echo "   It's recommended to create and activate a virtual environment first."
    echo ""
    echo "   To create a virtual environment:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

echo "📦 Installing Python dependencies..."
pip install --upgrade pip

# Install main requirements
echo "Installing core Django and API dependencies..."
pip install -r requirements.txt

echo "🧠 Installing Unstructured with extra formats..."
# Install Unstructured with additional format support
pip install "unstructured[pdf,docx,doc,txt,pptx,xlsx]==0.11.6"
pip install "unstructured-inference==0.7.23"

echo "🖼️  Installing OCR dependencies (optional)..."
# Install OCR capabilities (optional but recommended)
pip install pytesseract Pillow

echo "✅ Installation completed!"
echo ""
echo "🧪 Testing Unstructured installation..."

# Test the installation
python -c "
try:
    from unstructured.partition.auto import partition
    from unstructured.partition.text import partition_text
    elements = partition_text('Test document')
    print('✅ Unstructured is working correctly!')
    print(f'   Found {len(elements)} elements in test document')
except ImportError as e:
    print(f'❌ Import error: {e}')
except Exception as e:
    print(f'❌ Test failed: {e}')
"

echo ""
echo "🎯 Next steps:"
echo "1. Configure your environment variables (.env file)"
echo "2. Run database migrations: python manage.py migrate"
echo "3. Test the Unstructured endpoint: GET /api/ai_parser/test-unstructured/"
echo "4. Start the development server: python manage.py runserver"
echo ""
echo "📖 For more information, check the README.md file"
