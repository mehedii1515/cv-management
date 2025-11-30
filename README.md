# CV Management - AI-Powered Resume Parser & Intelligence Platform

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Django Version](https://img.shields.io/badge/Django-4.2.7-darkgreen.svg)](https://www.djangoproject.com)
[![React Version](https://img.shields.io/badge/React-18.2.0-61dafb.svg)](https://react.dev)
[![Next.js Version](https://img.shields.io/badge/Next.js-14.0.4-000000.svg)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cv--management-black.svg)](https://github.com/mehedii1515/cv-management)

**A professional-grade AI-powered resume parsing and CV management system with advanced search capabilities, built for enterprise talent management.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Documentation](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## 📌 Overview

CV Management is an enterprise-ready, full-stack application designed for efficient resume processing, intelligent data extraction, and comprehensive talent intelligence. It combines cutting-edge AI technologies (OpenAI GPT and Google Gemini) with robust full-text search capabilities to provide a complete solution for CV/resume management.

### Key Use Cases

- **Recruitment Firms**: Process high-volume resume submissions with automatic data extraction
- **HR Departments**: Centralized talent database with advanced search and filtering
- **Talent Acquisition**: Batch CV processing and intelligent candidate matching
- **Career Platforms**: Resume upload, parsing, and profile enrichment
- **Document Management**: Comprehensive CV indexing and retrieval system

---

## 🌟 Features

### 🔍 Document Processing
- **Multi-Format Support**: Parse PDF, DOCX, DOC, TXT, and RTF files
- **Advanced Text Extraction**: Unstructured library with Poppler integration for accurate PDF processing
- **Batch Processing**: Upload and process hundreds of resumes simultaneously
- **Quality Assessment**: Automatic quality scoring of parsed data
- **Format Conversion**: Automatic .doc to .docx conversion for enhanced extraction
- **OCR Capability**: Tesseract integration for scanned/image-based documents

### 🤖 AI Intelligence
- **Dual AI Engine**: 
  - **OpenAI GPT-4/3.5-turbo** (primary, highly accurate)
  - **Google Gemini 1.5** (fallback, cost-effective)
  - Automatic failover mechanism for reliability
- **Smart Data Extraction**:
  - Personal information (name, email, phone, DOB)
  - Professional details (employer, title, experience)
  - Skills and expertise areas
  - Education and certifications
  - Languages and certifications
  - Portfolio links and social profiles
- **NLP Processing**:
  - Token counting and truncation
  - Text normalization
  - Data validation and quality checks
  - Duplicate detection using content hashing

### 🔎 Advanced Search & Indexing
- **Elasticsearch Integration**:
  - Full-text search across resume content
  - Boolean operators (AND, OR, NOT)
  - Field-specific searching
  - Autocomplete suggestions
  - Result ranking and relevance scoring
- **DTSearch-like Functionality**: Complex query support similar to commercial solutions
- **Advanced Filtering**:
  - Filter by location, skills, sectors, experience level
  - Date range filtering
  - Multi-criteria advanced search
- **Real-time Indexing**: Automatic background indexing of new resumes via Celery

### 📊 Data Management
- **Comprehensive Resume Model**:
  - 50+ fields for complete talent profile
  - JSON fields for flexible data storage
  - 11 optimized database indices
  - Duplicate detection via content and person hashing
- **RESTful API**: 20+ endpoints for complete CRUD operations
- **Admin Panel**: Django admin interface for manual data management
- **Batch Operations**: Upload, reparse, and reindex multiple resumes

### 💻 User Interface
- **Modern Frontend**: Built with Next.js, React 18, and TypeScript
- **Component Library**: shadcn/ui components for consistent design
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Intuitive Workflows**: Tab-based navigation, drag-drop uploads, real-time feedback
- **Data Visualization**: Charts and statistics with Recharts
- **Form Handling**: React Hook Form with Zod validation

### 🔗 Integration Capabilities
- **QueryMind Integration**: Batch CV detection and classification from network drives
- **File Monitoring**: Automatic detection and processing of new resumes
- **Webhook Support**: Integration with external systems
- **API-First Design**: Easy integration with third-party applications

---

## 🏗️ Architecture

### System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                              │
│        Next.js + React + TypeScript + Tailwind CSS             │
│                    Port: 3000                                  │
└────────────────────┬───────────────────────────────────────────┘
                     │
                HTTP/REST
                     │
┌────────────────────▼───────────────────────────────────────────┐
│              API GATEWAY (Django REST)                         │
│              Port: 8000                                        │
│  ├─ CORS Middleware          ├─ Authentication                │
│  ├─ Rate Limiting            ├─ Input Validation              │
│  └─ Error Handling           └─ Request Logging               │
└────┬───────────────────────────────────────────┬───────────────┘
     │                                            │
     ├─────────────┬──────────────┬──────────┤
     │             │              │          │
     ▼             ▼              ▼          ▼
┌─────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐
│ Resumes │  │ AI Parse │  │ Search │  │  Core   │
│  App    │  │   App    │  │  App   │  │  App    │
└─────────┘  └──────────┘  └────────┘  └─────────┘
     │             │              │
     └──────────────┼──────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
        ▼                      ▼
    ┌───────────┐         ┌──────────────┐
    │ Celery    │         │ AI Services  │
    │ Tasks     │         │ (OpenAI,     │
    │           │         │  Gemini)     │
    └─────┬─────┘         └──────────────┘
          │
    ┌─────▼────────────────────────────────┐
    │     DATA LAYER                       │
    │                                      │
    │ ┌──────────┐  ┌─────────────────┐  │
    │ │ Database │  │ Elasticsearch   │  │
    │ │ (SQLite/ │  │ Search Indices  │  │
    │ │ PG)      │  └─────────────────┘  │
    │ │          │  ┌─────────────────┐  │
    │ │ • Resumes│  │ Redis Cache     │  │
    │ │ • Users  │  │ • Sessions      │  │
    │ │ • Audit  │  │ • Task Queue    │  │
    │ └──────────┘  └─────────────────┘  │
    └────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS | Modern web interface |
| **Backend** | Django 4.2.7, DRF 3.14.0 | REST API, business logic |
| **Database** | SQLite (dev), PostgreSQL (prod) | Data persistence |
| **Search** | Elasticsearch 7.17.0 | Full-text search & indexing |
| **Cache/Queue** | Redis 5.0.1, Celery 5.3.4 | Caching & async tasks |
| **AI Services** | OpenAI GPT, Google Gemini | Data extraction |
| **Document Processing** | Unstructured 0.18.11, Poppler 24.08.0 | Text extraction |
| **Web Server** | Gunicorn 21.2.0, Caddy/Nginx | Production serving |
| **Containerization** | Docker, Docker Compose | Deployment |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (3.11 or 3.12 recommended; 3.13+ not supported by Unstructured)
- **Node.js 16+**
- **Internet connection** (for API calls)
- **API Keys**: 
  - OpenAI API key (for resume parsing)
  - Google Gemini API key (optional, for fallback)

### Automated Setup (Recommended)

#### Windows
```bash
# Run automatic setup
setup.bat

# Edit .env with your API keys
# Then start servers
start_servers.bat
```

#### Linux/Mac
```bash
# Run automatic setup
./setup.sh

# Edit .env with your API keys
# Then start servers
./start_servers.sh
```

### Manual Setup

#### 1. Backend Setup
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

# Run migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 3. Configuration

Create `.env` file in backend directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default, optional for PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3
# DATABASE_URL=postgresql://user:password@localhost:5432/cvmanagement

# AI APIs (choose at least one)
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-gemini-key-here

# Elasticsearch (optional)
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Redis (optional, for Celery)
REDIS_URL=redis://localhost:6379

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/api/docs/ | Swagger documentation |
| Admin Panel | http://localhost:8000/admin/ | Data management |

---

## 📚 API Documentation

### Resume Management Endpoints

#### Create Resume
```http
POST /api/resumes/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "+1-234-567-8900",
  "location": "USA",
  "current_employer": "Tech Corp",
  "years_of_experience": 5
}
```

#### List Resumes
```http
GET /api/resumes/?page=1&page_size=10&search=python
```

#### Upload & Parse Resume
```http
POST /api/resumes/upload/
Content-Type: multipart/form-data

file: <resume file>
```

**Response:**
```json
{
  "id": "uuid-123",
  "status": "success",
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@example.com",
  "years_of_experience": 5,
  "skills": ["Python", "Django", "React"],
  "expertise_areas": ["Backend Development", "API Design"],
  "sectors": ["Technology"],
  "is_processed": true,
  "processing_status": "completed"
}
```

#### Search Resumes
```http
GET /api/search/?q=python+django&skills=python,react&experience_years_min=3
```

#### Advanced Search
```http
POST /api/search/advanced/
Content-Type: application/json

{
  "skills": ["Python", "Django"],
  "experience_years": {"min": 3, "max": 10},
  "sectors": ["Technology"],
  "location": ["USA", "Canada"],
  "availability": "immediate"
}
```

### Authentication

Include JWT token in request headers:
```http
Authorization: Bearer your-jwt-token-here
```

For detailed API documentation, visit: http://localhost:8000/api/docs/

---

## 🔄 System Workflows

### Workflow 1: Manual Resume Upload

```
User Upload → Browser Validation → File Selection
    ↓
POST /api/resumes/upload/
    ↓
Backend File Processing:
  1. Save file to media/uploads/
  2. Extract text (Unstructured)
  3. Parse with AI (OpenAI/Gemini)
  4. Validate data
  5. Store in database
    ↓
Post-Save Signal Triggered
    ↓
Background Task (Celery):
  1. Index in Elasticsearch
  2. Update search indices
  3. Calculate metrics
    ↓
Frontend Update:
  - Display success
  - Update resume list
  - Show resume card
```

### Workflow 2: Search Query

```
User Search Input → Query Validation
    ↓
GET /api/search/?q=...
    ↓
Backend Processing:
  1. Check Redis cache
  2. Build Elasticsearch query
  3. Apply filters
  4. Execute search
    ↓
Result Processing:
  1. Rank by relevance
  2. Format results
  3. Add pagination
  4. Cache result (5 min)
    ↓
Frontend Display:
  - Show results
  - Enable pagination
  - Highlight matches
```

### Workflow 3: QueryMind Batch Processing

```
python QueryMind/main.py
    ↓
1. Initialize & Load Configuration
    ↓
2. Scan Network Directory
    ↓
3. For Each File (Batch: 1000):
   ├─ Extract text
   ├─ Tokenize (max 500)
   ├─ AI Classification (Is Resume?)
   └─ If Yes: Upload to Backend
    ↓
4. Background Indexing:
   ├─ Elasticsearch indexing
   ├─ Search availability
    ↓
5. Generate Output:
   ├─ tokens.json
   ├─ Resume_Classification.xlsx
   └─ Statistics report
```

---

## 🗂️ Project Structure

```
cv-management/
├── backend/                      # Django REST Framework backend
│   ├── apps/
│   │   ├── resumes/             # Resume CRUD & management
│   │   ├── ai_parser/           # AI extraction service
│   │   ├── search/              # Elasticsearch integration
│   │   └── core/                # Shared utilities
│   ├── resume_parser/           # Django project settings
│   ├── media/                   # Uploaded files
│   ├── logs/                    # Application logs
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                     # Next.js React frontend
│   ├── src/
│   │   ├── app/                 # Pages
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── lib/                 # Utilities
│   │   └── types/               # TypeScript types
│   ├── package.json
│   └── tsconfig.json
│
├── QueryMind/                    # CV detection & classification
│   ├── main.py                  # Main processing script
│   ├── Include/                 # Shared utilities
│   └── requirements.txt
│
├── docummentation/              # Comprehensive guides
│   ├── SETUP_GUIDE.md
│   ├── USER_MANUAL.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── ...
│
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Docker build config
├── setup.bat / setup.sh         # Automated setup
└── README.md                    # This file
```

For detailed folder analysis, see: [FOLDER_ANALYSIS_AND_WORKFLOW.md](FOLDER_ANALYSIS_AND_WORKFLOW.md)

---

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build and run all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Admin Panel: http://localhost:8000/admin/
```

### Docker Compose Services

- **PostgreSQL**: Database (port 5432)
- **Redis**: Cache and task queue (port 6379)
- **Elasticsearch**: Search engine (port 9200)
- **Backend**: Django API (port 8000)
- **Frontend**: Next.js app (port 3000)

---

## 🚀 Production Deployment

### Prerequisites for Production

- PostgreSQL 13+ (recommended over SQLite)
- Redis for caching and Celery
- Elasticsearch cluster (3+ nodes for HA)
- Multiple Gunicorn/Celery workers
- Load balancer (Nginx/Caddy)
- SSL/TLS certificates

### Deployment Steps

#### 1. Environment Setup
```bash
# Use production settings
export DJANGO_SETTINGS_MODULE=resume_parser.production_settings

# Set environment variables
export SECRET_KEY=your-production-secret-key
export DEBUG=False
export DATABASE_URL=postgresql://...
export OPENAI_API_KEY=...
```

#### 2. Database Migration
```bash
python manage.py migrate
python manage.py collectstatic
```

#### 3. Start Services
```bash
# Start Django with Gunicorn
gunicorn resume_parser.wsgi:application --workers 4 --bind 0.0.0.0:8000

# Start Celery worker
celery -A resume_parser worker -l info

# Start Celery beat (for scheduled tasks)
celery -A resume_parser beat -l info

# Start Next.js production server
npm run build && npm start
```

#### 4. Reverse Proxy Configuration (Caddy)
```
resume-parser.yourdomain.com {
    reverse_proxy /api/* localhost:8000
    reverse_proxy /* localhost:3000
    
    encode gzip
    
    file_server /static/* {
        root /path/to/backend/staticfiles
    }
}
```

See [DEPLOYMENT_GUIDE.md](docummentation/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📊 Extracted Data Fields

The system extracts comprehensive resume information:

```
Personal Information
├── Name (First, Last)
├── Email
├── Phone
└── Location

Professional Details
├── Current Title
├── Current Employer
├── Total Experience (years & months)
├── Work Arrangement Preference
└── Availability

Skills & Expertise
├── Technical Skills
├── Soft Skills
├── Domain Expertise
└── Proficiency Levels

Education
├── Degrees
├── Institutions
├── Graduation Year
└── GPA/Honors

Additional
├── Languages Spoken
├── Certifications
├── Associations
├── Publications
├── Portfolio Links
└── Social Profiles
```

---

## 🔍 Search Capabilities

### Basic Search
```
GET /api/search/?q=python+developer
```

### Boolean Search (DTSearch-like)
```
GET /api/search/boolean/?q=Python+AND+Django+NOT+Javascript
```

### Advanced Filtering
```
GET /api/search/advanced/?skills=python,django&location=USA&experience_min=3&experience_max=10
```

### Autocomplete Suggestions
```
GET /api/search/suggest/?q=dev
```

---

## 🔐 Security Features

- **Authentication**: Django session and JWT token support
- **CORS**: Configurable cross-origin resource sharing
- **CSRF Protection**: Django CSRF middleware
- **Input Validation**: Comprehensive input validation
- **SQL Injection Prevention**: ORM parameterized queries
- **File Upload Security**: Type validation and size limits
- **HTTPS/TLS**: SSL/TLS support in production
- **Password Security**: PBKDF2 hashing with salt
- **Rate Limiting**: Configurable API rate limits

---

## 📈 Performance & Scalability

### Current Setup (Development)
- SQLite database
- Single Django process
- Suitable for: ~10 concurrent users

### Recommended Production
- PostgreSQL with connection pooling
- Multiple Gunicorn workers
- Redis cache layer
- Elasticsearch cluster
- Celery worker pool
- Suitable for: ~100 concurrent users

### Enterprise Scale
- PostgreSQL cluster with replication
- Kubernetes orchestration
- Horizontal auto-scaling
- CDN for static assets
- Distributed caching
- Suitable for: 1000+ concurrent users

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
python manage.py test apps.resumes
python manage.py test apps.search
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
python complete_workflow_demo.py
```

---

## 🔧 Troubleshooting

### Python Version Issues
```bash
# Check Python version (must be 3.10+)
python --version

# Unstructured library requires Python < 3.13
```

### PDF Processing Issues
```bash
# Poppler must be in PATH
# Check installation:
which pdftotext  # Linux/Mac
where pdftotext  # Windows
```

### Elasticsearch Connection
```bash
# Ensure Elasticsearch is running
curl localhost:9200

# If not running:
elasticsearch  # Linux/Mac
# Or use Docker: docker run -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:7.17.0
```

### API Key Errors
```bash
# Verify API keys in .env
# Check file permissions
# Ensure keys have required permissions
```

See [USER_MANUAL.md](docummentation/USER_MANUAL.md) for more troubleshooting.

---

## 📚 Documentation

- **[SETUP_GUIDE.md](docummentation/SETUP_GUIDE.md)** - Detailed setup instructions
- **[USER_MANUAL.md](docummentation/USER_MANUAL.md)** - Complete user guide
- **[DEPLOYMENT_GUIDE.md](docummentation/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[FILE_INDEX_SEARCH_GUIDE.md](docummentation/FILE_INDEX_SEARCH_GUIDE.md)** - Search system
- **[POSTGRESQL_SETUP.md](docummentation/POSTGRESQL_SETUP.md)** - Database setup
- **[CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md)** - Detailed code analysis
- **[FOLDER_ANALYSIS_AND_WORKFLOW.md](FOLDER_ANALYSIS_AND_WORKFLOW.md)** - System architecture

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push to GitHub
6. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support & Contact

- **Repository**: [github.com/mehedii1515/cv-management](https://github.com/mehedii1515/cv-management)
- **Issues**: [GitHub Issues](https://github.com/mehedii1515/cv-management/issues)
- **Documentation**: See `/docummentation/` folder
- **Contact**: [Open an issue](https://github.com/mehedii1515/cv-management/issues)

---

## 🔮 Roadmap

### Upcoming Features
- [ ] Machine learning-based entity extraction
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] Microservices architecture
- [ ] API rate limiting tokens
- [ ] Advanced caching strategies
- [ ] GraphQL API support
- [ ] WebSocket real-time updates

---

## 📊 Project Statistics

```
Backend Code
├─ Python files: 30+
├─ Lines of code: 15,000+
├─ Models: 4+
├─ API endpoints: 20+
└─ Services: 5+

Frontend Code
├─ TypeScript/React files: 50+
├─ Lines of code: 8,000+
├─ Components: 30+
├─ Pages: 5+
└─ Custom hooks: 10+

Database
├─ Tables: 10+
├─ Indices: 11+ (optimized)
└─ Fields: 50+ resume fields

External Integrations
├─ OpenAI GPT
├─ Google Gemini
├─ Elasticsearch
├─ PostgreSQL
├─ Redis
└─ Celery
```

---

## 🙏 Acknowledgments

- Django and Django REST Framework teams
- Next.js and React teams
- OpenAI and Google for AI APIs
- Elasticsearch team
- shadcn/ui for component library
- All contributors and users

---

## 📝 Changelog

### Version 1.0.0 (Current)
- Initial production release
- Full resume parsing capabilities
- Elasticsearch integration
- QueryMind batch processing
- Docker support
- Comprehensive documentation

---

<div align="center">

**Built with ❤️ by the CV Management Team**

[⬆ Back to top](#cv-management---ai-powered-resume-parser--intelligence-platform)

</div>
