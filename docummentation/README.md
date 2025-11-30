# Resume Parser - AI-Powered Document Processing

An intelligent resume parsing platform that leverages OpenAI GPT and Google Gemini AI to extract structured data from resumes and provide comprehensive talent intelligence.

## �️ Setup Instructions

### Quick Setup
**Windows:** `setup.bat` → Edit `.env` → `start_servers.bat`
**Linux/Mac:** `./setup.sh` → Edit `.env` → `./start_servers.sh`

## 📋 Requirements

- **Python 3.10, 3.11, or 3.12** (3.13+ not supported by unstructured library)
- **Node.js 16+** (for frontend)
- **Internet connection** (for package downloads and AI API calls)

## 🔑 API Keys Setup

You'll need API keys from at least one AI provider:

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`

### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or sign in to your Google account
3. Generate an API key
4. Add to `.env`: `GOOGLE_API_KEY=your-key-here`

## 🌐 Application URLs

- **Frontend Application**: http://localhost:3000/
- **Backend API**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## ⚡ Features

- **Multi-format Support**: Parse PDF, DOCX, DOC, TXT files
- **Dual AI Processing**: OpenAI GPT + Google Gemini with fallback capability
- **Advanced Document Processing**: Powered by Unstructured library for superior text extraction
- **Smart Extraction**: Contact info, skills, experience, education, and more
- **Quality Scoring**: Automatic quality assessment of parsed data
- **Batch Processing**: Upload multiple resumes at once
- **Modern Web Interface**: Next.js frontend with Tailwind CSS
- **RESTful API**: Django REST Framework backend
- **Admin Interface**: Django admin for data management

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | Django REST Framework, Python |
| Database | SQLite (default) / PostgreSQL |
| AI Integration | OpenAI GPT, Google Gemini API |
| File Processing | Unstructured, Poppler, Python |

## 🗂️ Project Structure

```
resume-parser/
├── backend/              # Django backend
│   ├── apps/
│   │   ├── ai_parser/   # AI processing logic
│   │   ├── resumes/     # Resume management
│   │   └── core/        # Core utilities
│   ├── media/           # Uploaded files
│   ├── venv/            # Python virtual environment
│   └── manage.py        # Django management
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/         # App router pages
│   │   ├── components/  # React components
│   │   └── lib/         # Utility functions
│   └── package.json
├── setup.bat            # Windows automatic setup
├── setup.sh             # Linux/Mac automatic setup
├── start_servers.bat    # Windows server launcher
├── start_servers.sh     # Linux/Mac server launcher
└── README.md            # This file
```

## 📋 Extracted Data Fields

- **Personal Information**: Name, Email, Phone, Location
- **Professional Details**: Experience, Current Employer, Availability
- **Skills & Expertise**: Technical skills, soft skills, expertise areas
- **Education**: Degrees, certifications, institutions
- **Languages**: Language proficiency levels
- **Industries & Sectors**: Work domain experience
- **Portfolio**: Website links, professional profiles

## 🏗️ Manual Setup (Advanced)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Setup database
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start frontend server
npm run dev
```

## ⚙️ Configuration Options

### AI Provider Settings
Edit `backend/.env`:

- `AI_PROVIDER=both` - Use both OpenAI and Gemini with fallback
- `AI_PROVIDER=openai` - Use only OpenAI
- `AI_PROVIDER=gemini` - Use only Gemini

### File Upload Settings
- `MAX_UPLOAD_SIZE=10485760` - Maximum file size (10MB)
- `ALLOWED_FILE_TYPES=pdf,docx,txt` - Supported file types

### Model Configuration
- `OPENAI_MODEL=gpt-4o-mini` - OpenAI model to use
- `GEMINI_MODEL=gemini-1.5-flash` - Gemini model to use

## 🛠️ Troubleshooting

### Python Version Issues
```bash
# Check your Python version
python --version

# If you have Python 3.13+, install an older version
# Use pyenv, conda, or download from python.org
```

### Poppler Issues (PDF Processing)
**Windows**: The setup script automatically downloads Poppler
**Linux**: `sudo apt-get install poppler-utils`
**Mac**: `brew install poppler`

### Permission Issues (Linux/Mac)
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x start_servers.sh
chmod +x stop_servers.sh
```

### Port Already in Use
```bash
# Check what's using the ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill processes if needed
kill -9 <PID>
```

### Missing Dependencies
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

## 🔧 Development

### Adding New Features
1. Backend changes go in `backend/apps/`
2. Frontend changes go in `frontend/src/`
3. Database changes need migrations: `python manage.py makemigrations`

### Testing
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### API Documentation
Visit http://localhost:8000/api/ when the backend is running

## 🐛 Common Issues

1. **"No module named..."**: Virtual environment not activated
2. **"Unable to get page count"**: Poppler not installed or not in PATH
3. **"Connection refused"**: Server not started or wrong port
4. **"API key invalid"**: Check your API keys in .env file
5. **"Permission denied"**: Run setup scripts as administrator (Windows) or use sudo (Linux/Mac)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs in `backend/server.log`
3. Ensure all requirements are met
4. Verify API keys are correctly set

## 🔒 Security Notes

- Keep your API keys secure and never commit them to version control
- For production deployment, set `DEBUG=False` in `.env`
- Use strong `SECRET_KEY` in production
- Consider using environment variables instead of `.env` file in production

## 📜 License

This project is for educational and development purposes. Please ensure you comply with the terms of service for OpenAI and Google AI services. 