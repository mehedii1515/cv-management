# DOCX to PDF Conversion Setup Guide

This guide helps you set up DOCX to PDF conversion for your file viewer system.

## 🎯 What This Does

Instead of showing unformatted text for DOCX files, the system will now:
- Convert DOCX files to PDF on-the-fly
- Display them in the browser with original formatting preserved
- Provide options to view as PDF or download the original DOCX

## 📋 Setup Options

### Option 1: LibreOffice (Recommended - Best Quality)

#### Windows:
1. Download LibreOffice from: https://www.libreoffice.org/download/download/
2. Install LibreOffice
3. Add LibreOffice to your PATH:
   - Find LibreOffice installation directory (usually `C:\Program Files\LibreOffice\program\`)
   - Add this path to your system PATH environment variable
   - OR use Chocolatey: `choco install libreoffice`

#### Linux/macOS:
```bash
# Run the installation script
chmod +x install_libreoffice.sh
./install_libreoffice.sh
```

### Option 2: Python Libraries (Fallback)

Install the Python conversion libraries:

```bash
# Navigate to backend directory
cd backend

# Install additional requirements
pip install -r docx_conversion_requirements.txt
```

**Note**: Some libraries may require additional system dependencies:
- `weasyprint` requires: libffi-dev, libxml2-dev, libxslt-dev, libcairo2-dev, libpango1.0-dev
- On Ubuntu: `sudo apt-get install libffi-dev libxml2-dev libxslt-dev libcairo2-dev libpango1.0-dev`

### Option 3: Docker (Isolated Environment)

If you prefer Docker, create a Dockerfile with LibreOffice:

```dockerfile
FROM python:3.9
RUN apt-get update && apt-get install -y libreoffice --no-install-recommends
# ... rest of your app setup
```

## 🧪 Testing the Setup

1. Start your backend server:
   ```bash
   cd backend
   python manage.py runserver 8000
   ```

2. Test the conversion endpoint directly:
   ```
   GET http://localhost:8000/api/search/files/docx-pdf?path=/path/to/your/file.docx
   ```

3. You should receive a PDF file response.

## 🚀 How It Works

1. **Frontend**: When a DOCX file is clicked, instead of showing text extraction options, it displays an iframe with the PDF conversion URL
2. **Backend**: The `/api/search/files/docx-pdf` endpoint:
   - Receives the DOCX file path
   - Converts it to PDF using available methods (LibreOffice → python-docx2pdf → HTML conversion)
   - Returns the PDF for browser display
   - Cleans up temporary files

## 🔧 Troubleshooting

### LibreOffice Issues:
- Ensure `libreoffice` command is available in terminal
- On Windows, check PATH environment variable
- Try running: `libreoffice --headless --version`

### Python Library Issues:
- Install system dependencies for weasyprint
- Try individual package installation: `pip install docx2pdf`

### Permission Issues:
- Ensure the application has write permissions to create temporary files
- Check file paths are accessible

## 📱 Frontend Changes

The file viewer now shows DOCX files like this:
- **Header**: "filename.docx (as PDF)"
- **Buttons**: 
  - "Open PDF in New Tab" - opens the converted PDF
  - "Download Original DOCX" - downloads the original file
- **Content**: PDF iframe with the converted document

## 🎨 Benefits

✅ **Original formatting preserved** - No more unformatted text  
✅ **In-browser viewing** - No need for external applications  
✅ **Multiple fallback methods** - Works even if one method fails  
✅ **Clean interface** - Professional PDF viewer experience  
✅ **Cross-platform** - Works on Windows, Linux, macOS  

## 📝 Next Steps

1. Choose and install your preferred conversion method
2. Test with a sample DOCX file
3. Verify the formatting looks correct in the PDF viewer
4. Enjoy formatted document viewing! 🎉
