# AI-Powered Resume Parser Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+ (see [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for installation guide)
- Google Gemini API Key

### 1. Database Setup
```bash
# Option 1: Using provided SQL script (recommended)
sudo -u postgres psql -f setup_database.sql

# Option 2: Manual setup
sudo -u postgres psql
CREATE DATABASE resume_parser;
CREATE USER resume_parser_user WITH PASSWORD 'secure_password_change_me';
GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_parser_user;
ALTER USER resume_parser_user CREATEDB;
\q
```

### 2. Environment Setup
```bash
cp env.example .env
# Edit .env with your database credentials and Gemini API key
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Docs: http://localhost:8000/api/docs/

## 🏗️ Architecture

### Backend (Django + PostgreSQL)
- Django REST Framework API
- PostgreSQL database with indexed tables
- Google Gemini AI integration
- File processing (PDF, DOCX, TXT)

### Frontend (Next.js + TypeScript)
- Modern React dashboard
- Tailwind CSS + shadcn/ui
- Real-time updates
- Advanced search & filtering

## 📋 Key Features

### Resume Processing
- Multi-format file upload
- AI-powered data extraction
- 20+ structured fields
- Duplicate detection

### Dashboard
- Resume management
- Search & filtering
- Statistics & analytics
- Export capabilities

## 🔧 Configuration

### Required Environment Variables
```env
# Database
DB_NAME=resume_parser
DB_USER=resume_parser_user
DB_PASSWORD=secure_password_change_me
DB_HOST=localhost
DB_PORT=5432

# AI
GEMINI_API_KEY=your-api-key-here
```

## 📚 API Endpoints

- `POST /api/resumes/upload/` - Upload resume
- `GET /api/resumes/` - List resumes
- `GET /api/resumes/stats/` - Get statistics
- `GET /api/health/` - Health check

## 🚀 Production Deployment

1. Update environment for production
2. Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)
3. Configure proper secrets and SSL
4. Set up monitoring and backups

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Submit pull request

Built with ❤️ using Django, Next.js, and Google Gemini AI 