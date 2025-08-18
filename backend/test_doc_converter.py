#!/usr/bin/env python
"""
Test script to check if DOC to DOCX conversion is working
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.ai_parser.doc_converter import doc_converter

def test_doc_converter():
    """Test the DOC converter functionality"""
    print("🔧 Testing DOC to DOCX Converter")
    print("=" * 50)
    
    # Check if LibreOffice is available
    if doc_converter.is_available():
        print("✅ LibreOffice is available for DOC conversion")
        print(f"   LibreOffice command: {doc_converter.libreoffice_cmd}")
    else:
        print("❌ LibreOffice is NOT available")
        print("   DOC files will be processed using unstructured library's conversion")
        print("   To enable direct DOC→DOCX conversion, install LibreOffice:")
        print("   - Windows: Download from https://www.libreoffice.org/")
        print("   - Linux: sudo apt-get install libreoffice")
        print("   - macOS: brew install --cask libreoffice")
    
    print("\n📋 Summary:")
    print(f"   DOC conversion available: {doc_converter.is_available()}")
    
    return doc_converter.is_available()

if __name__ == "__main__":
    test_doc_converter()
