# CV Management - AI-Powered Resume Parser & Intelligence Platform

An intelligent resume parsing and CV management platform that leverages OpenAI GPT and Google Gemini AI to extract structured data from resumes, classify CVs, and provide comprehensive talent intelligence with advanced search capabilities.

## 🎯 Project Overview

This is a full-stack application designed to:
- Parse multiple document formats (PDF, DOCX, DOC, TXT, RTF)
- Extract structured talent data using advanced AI models
- Classify and organize CVs by sectors and experience levels
- Provide batch processing capabilities for large document uploads
- Enable intelligent search and filtering across parsed resume data
- Integrate with third-party systems for continuous CV processing

## 📋 Key Features

### Document Processing
- **Multi-format Support**: PDF, DOCX, DOC, TXT, RTF files
- **Advanced Text Extraction**: Powered by Unstructured library with Poppler for PDF handling
- **Batch Processing**: Upload and process multiple resumes simultaneously
- **Quality Scoring**: Automatic quality assessment of extracted data

### AI & Intelligence
- **Dual AI Engine**: OpenAI GPT + Google Gemini with automatic fallback
- **Smart Extraction**: Contact info, skills, experience, education, certifications
- **NLP Processing**: Token counting, text normalization, data validation
- **Sector Classification**: Automatic categorization by industry/sector

### Data Management
- **Advanced Search**: Elasticsearch integration for full-text search
- **File Indexing**: Efficient file discovery and reindexing capabilities
- **Resume Management**: CRUD operations with audit trails
- **Database Options**: SQLite (default) or PostgreSQL

### User Interface
- **Modern Frontend**: Next.js with TypeScript, Tailwind CSS, and shadcn/ui components
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Admin Interface**: Django admin panel for data management
- **RESTful API**: Comprehensive API documentation with drf-spectacular

## 🏗️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Django | 4.2.7 |
| **API Framework** | Django REST Framework | 3.14.0 |
| **Frontend** | Next.js | 14.0.4 |
| **Frontend UI** | React + shadcn/ui | 18.2.0 |
| **Styling** | Tailwind CSS | Latest |
| **Database** | SQLite / PostgreSQL | 14+ |
| **Search Engine** | Elasticsearch | 7.17.0 |
| **Document Processing** | Unstructured | 0.18.11 |
| **PDF Handling** | Poppler | 24.08.0 |
| **OCR Support** | Tesseract | 0.3.10 |
| **AI APIs** | OpenAI GPT, Google Gemini | Latest |
| **Task Queue** | Celery + Redis | 5.3.4, 5.0.1 |
| **Web Server** | Gunicorn | 21.2.0 |

## 🗂️ Project Structure

```
cv-management/
├── backend/                          # Django REST API & Core Logic
│   ├── apps/
│   │   ├── ai_parser/               # AI parsing & extraction logic
│   │   │   ├── models.py            # ParseResult, ExtractedData models
│   │   │   ├── serializers.py       # Data serialization
│   │   │   ├── views.py             # API endpoints
│   │   │   └── parser_engine.py     # GPT/Gemini integration
│   │   ├── resumes/                 # Resume management
│   │   │   ├── models.py            # Resume, ResumeFile models
│   │   │   ├── views.py             # CRUD endpoints
│   │   │   └── serializers.py       # Resume serialization
│   │   ├── search/                  # Search & indexing
│   │   │   ├── models.py            # Search indices
│   │   │   ├── documents.py         # Elasticsearch documents
│   │   │   ├── views.py             # Search endpoints
│   │   │   ├── file_views.py        # File search handlers
│   │   │   ├── signals.py           # Index update signals
│   │   │   └── management/
│   │   │       └── commands/
│   │   │           └── reindex_files.py  # Reindex management command
│   │   └── core/                    # Shared utilities
│   │       ├── utils.py             # Helper functions
│   │       └── validators.py        # Data validators
│   ├── media/                        # Uploaded resume files
│   ├── logs/                         # Application logs
│   ├── staticfiles/                  # Collected static files
│   ├── poppler-24.08.0/             # Poppler PDF library
│   ├── db.sqlite3                   # SQLite database
│   ├── manage.py                    # Django CLI
│   ├── requirements.txt             # Python dependencies
│   ├── production_requirements.txt  # Production-specific deps
│   ├── resume_parser/               # Django project settings
│   │   ├── settings.py              # Configuration
│   │   ├── production_settings.py   # Production config
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  # WSGI entry point
│   └── setup_poppler_env.sh         # Poppler environment setup
│
├── frontend/                         # Next.js React Application
│   ├── src/
│   │   ├── app/                     # App router pages
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── page.tsx             # Home page
│   │   │   ├── upload/              # Upload feature
│   │   │   ├── search/              # Search feature
│   │   │   ├── results/             # Results display
│   │   │   └── admin/               # Admin interface
│   │   ├── components/              # Reusable React components
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── forms/               # Form components
│   │   │   └── layout/              # Layout components
│   │   └── lib/                     # Utility functions
│   │       ├── api.ts               # API client
│   │       ├── hooks.ts             # Custom React hooks
│   │       └── utils.ts             # Helper utilities
│   ├── public/                      # Static assets
│   ├── package.json                 # Node dependencies
│   ├── tsconfig.json                # TypeScript config
│   ├── tailwind.config.js           # Tailwind config
│   ├── next.config.js               # Next.js config
│   └── components.json              # shadcn/ui config
│
├── QueryMind/                        # CV Processing & Classification Engine
│   ├── main.py                      # Main processing workflow
│   ├── enhanced_main.py             # Enhanced version with improvements
│   ├── cv_monitoring_service.py     # Monitor new CV uploads
│   ├── requirements.txt             # QueryMind dependencies
│   ├── processed_files.txt          # Log of processed files
│   ├── Include/                     # Shared utilities
│   │   ├── Config.py                # Configuration settings
│   │   ├── Filestream.py            # File operations
│   │   └── Integration.py           # Django integration
│   └── Resume_Classification.xlsx   # Output classification results
│
├── docummentation/                  # Project Documentation
│   ├── README.md                    # Original documentation
│   ├── SETUP_GUIDE.md               # Setup instructions
│   ├── USER_MANUAL.md               # User guide
│   ├── DEPLOYMENT_GUIDE.md          # Production deployment
│   ├── PRODUCTION_DEPLOYMENT_GUIDE.md
│   ├── POSTGRESQL_SETUP.md          # Database setup
│   ├── DOCX_PDF_CONVERSION_SETUP.md # Document conversion
│   ├── FILE_INDEX_SEARCH_GUIDE.md   # Search system
│   ├── FIREWALL_SETUP_PC.md         # Network setup
│   ├── USER_INSTRUCTIONS.md         # User instructions
│   ├── OFFICE_ACCESS_GUIDE.md       # Office network access
│   └── dtSearch_Desktop.pdf         # Search system documentation
│
├── Setup & Configuration Scripts
│   ├── setup.bat                    # Windows automatic setup
│   ├── setup.sh                     # Linux/Mac automatic setup
│   ├── start_servers.bat            # Windows server launcher
│   ├── start_servers.sh             # Linux/Mac server launcher
│   ├── start_production.bat         # Production startup (Windows)
│   ├── stop_production.bat          # Production shutdown (Windows)
│   ├── stop_servers.sh              # Server shutdown (Linux/Mac)
│   ├── start_network.sh             # Network startup
│   ├── switch-mode.sh               # Development/Production mode switcher
│   ├── setup_database.sql           # Database schema
│   ├── CREATE_POSTGRES_PORTABLE.bat # PostgreSQL portable setup
│   └── export_database.bat          # Database export/backup
│
├── Deployment & Production
│   ├── Caddyfile                    # Caddy reverse proxy config
│   ├── render.yaml                  # Render deployment config
│   ├── .env                         # Environment variables (secret)
│   ├── .env.example                 # Environment template
│   └── production_settings.py       # Production configuration
│
└── Workflow & Integration
    ├── complete_workflow_demo.py    # End-to-end workflow example
    ├── complete_integration_demo.py # Integration demonstration
    ├── integration_manager.py       # Integration orchestration
    ├── monitor_integration.py       # Monitor integration health
    ├── reparse_resume.py            # Reparse existing resumes
    └── test_*.py                    # Various test files
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (3.11 or 3.12 recommended)
- **Node.js 16+**
- **Internet connection** (for API calls)
- **API Keys**: OpenAI or Google Gemini (or both)

### 1️⃣ Automatic Setup

**Windows:**
```bash
setup.bat
# Edit .env with your API keys
start_servers.bat
```

**Linux/Mac:**
```bash
./setup.sh
# Edit .env with your API keys
./start_servers.sh
```

### 2️⃣ Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3️⃣ Configuration

Create `.env` file in the backend directory:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, uses SQLite by default)
DATABASE_URL=postgresql://user:password@localhost/cvmanagement

# API Keys (choose at least one)
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-gemini-key

# Elasticsearch (optional)
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Redis (for Celery)
REDIS_URL=redis://localhost:6379

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🌐 Access Points

| Component | URL | Default Credentials |
|-----------|-----|-------------------|
| Frontend | http://localhost:3000 | - |
| Backend API | http://localhost:8000 | - |
| API Documentation | http://localhost:8000/api/schema/ | - |
| Admin Panel | http://localhost:8000/admin/ | Create during setup |

## 📝 Extracted Data Fields

The system extracts comprehensive information from resumes:

```
Personal Information
├── Name
├── Email
├── Phone
└── Location

Professional Details
├── Current Title
├── Current Employer
├── Years of Experience
├── Industry/Sector
└── Availability Status

Skills & Expertise
├── Technical Skills
├── Soft Skills
├── Domain Expertise
└── Certifications

Education
├── Degrees
├── Institutions
├── Graduation Year
└── GPA/Honors

Languages
├── Languages Spoken
└── Proficiency Levels

Additional
├── Website/Portfolio Links
├── LinkedIn Profile
├── Publications
└── References
```

## 🔌 API Endpoints

### Resume Management
- `POST /api/resumes/` - Create resume
- `GET /api/resumes/` - List resumes
- `GET /api/resumes/{id}/` - Get resume details
- `DELETE /api/resumes/{id}/` - Delete resume

### File Upload & Parsing
- `POST /api/resumes/upload/` - Upload and parse resume
- `GET /api/resumes/{id}/parsed-data/` - Get parsed data
- `POST /api/resumes/{id}/reparse/` - Reparse resume

### Search
- `GET /api/search/` - Full-text search
- `POST /api/search/advanced/` - Advanced filtering
- `POST /api/search/reindex/` - Reindex search database

### AI Processing
- `POST /api/ai-parser/extract/` - Extract from text
- `GET /api/ai-parser/status/` - Check processing status

## 🛠️ Common Tasks

### Upload Resumes Programmatically
```python
import requests

files = {'file': open('resume.pdf', 'rb')}
response = requests.post(
    'http://localhost:8000/api/resumes/upload/',
    files=files
)
print(response.json())
```

### Batch Process CVs from Network Drive
```bash
# Edit QueryMind/main.py to point to your CV folder
# Then run:
python QueryMind/main.py
```

### Reindex Search Database
```bash
cd backend
python manage.py reindex_files
```

### Export Database
```bash
# Windows
export_database.bat

# Linux/Mac
python backend/manage.py dumpdata > backup.json
```

## 🔍 Search Capabilities

### Basic Search
```bash
GET /api/search/?q=python
```

### Advanced Search
```bash
POST /api/search/advanced/
{
  "skills": ["Python", "Django"],
  "experience_years": {"min": 3, "max": 10},
  "sectors": ["Technology"],
  "availability": "immediate"
}
```

## 📊 Production Deployment

### Using Caddy Reverse Proxy
```bash
# Ensure Caddyfile is configured
caddy start

# Application will be available at configured domain
```

### Using Render
```bash
# Deploy using render.yaml configuration
render deploy
```

### Docker Deployment
```bash
# Build Docker image
docker build -t cv-management .

# Run container
docker run -p 8000:8000 -p 3000:3000 cv-management
```

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Rotate API keys regularly
3. **Database**: Use strong passwords in production
4. **CORS**: Configure CORS properly in production
5. **SSL/TLS**: Use HTTPS in production
6. **Admin Access**: Restrict admin panel access
7. **File Uploads**: Validate and scan uploaded files
8. **Rate Limiting**: Implement rate limiting on API endpoints

## 🐛 Troubleshooting

### Python Version Issues
```bash
# Ensure Python 3.10+
python --version

# Unstructured library requires Python < 3.13
```

### PDF Processing Issues
```bash
# Poppler must be in the system PATH
# Or set explicitly in settings.py
POPPLER_PATH = "/path/to/poppler/bin"
```

### Elasticsearch Connection
```bash
# Ensure Elasticsearch is running
curl localhost:9200

# If not running, start it:
# Windows: Use Elasticsearch service
# Linux/Mac: elasticsearch
```

### API Key Errors
```bash
# Verify API keys are set correctly
# Check .env file permissions
# Ensure keys have required permissions
```

## 📚 Documentation

- **[SETUP_GUIDE.md](docummentation/SETUP_GUIDE.md)** - Detailed setup instructions
- **[USER_MANUAL.md](docummentation/USER_MANUAL.md)** - How to use the system
- **[DEPLOYMENT_GUIDE.md](docummentation/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[FILE_INDEX_SEARCH_GUIDE.md](docummentation/FILE_INDEX_SEARCH_GUIDE.md)** - Search system documentation
- **[POSTGRESQL_SETUP.md](docummentation/POSTGRESQL_SETUP.md)** - Database setup

## 🧪 Testing

```bash
# Run Django tests
cd backend
python manage.py test

# Run frontend tests
cd frontend
npm test

# Run integration tests
python complete_workflow_demo.py
```

## 📈 Performance Optimization

### Database
- Create indices on frequently searched fields
- Use PostgreSQL for production
- Regular database backups

### Caching
- Enable Redis caching for API responses
- Cache parsed resume data
- Use browser caching for static assets

### Batch Processing
- Process resumes in batches of 100-1000
- Use Celery for async tasks
- Monitor memory usage during batch operations

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push to GitHub
6. Create a Pull Request

## 📄 License

[Specify your license here]

## 👥 Support

For issues, questions, or suggestions:
- Check existing documentation
- Review the troubleshooting section
- Contact the development team

## 🔗 External Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Google Gemini API](https://aistudio.google.com/)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

## 📊 System Architecture

```
┌─────────────────┐
│  Frontend UI    │ (Next.js + React)
│  (Port 3000)    │
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│  Django API     │ (Django REST Framework)
│  (Port 8000)    │
├─────────────────┤
│ • Resume CRUD   │
│ • AI Processing │
│ • Search Engine │
│ • File Upload   │
└────────┬────────┘
    ┌───┴──────┬────────────┐
    │           │            │
┌───▼──┐  ┌────▼────┐  ┌───▼─────┐
│SQLite│  │OpenAI   │  │Elastic  │
│/PG   │  │/Gemini  │  │search   │
└──────┘  └─────────┘  └─────────┘
```

## 📝 Recent Updates

- **2025-11-30**: Documentation reorganization and README enhancement
- Added comprehensive API endpoint documentation
- Improved project structure documentation
- Enhanced deployment guidelines

---

**Last Updated**: November 30, 2025  
**Repository**: cv-management  
**Branch**: feature/typescript-fixes-and-production-setup
