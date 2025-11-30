# Resume Parser with QueryMind Integration - Complete User Manual

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [QueryMind Integration](#querymind-integration)
5. [User Interface Guide](#user-interface-guide)
6. [Search Functionality](#search-functionality)
7. [Deployment Guide](#deployment-guide)
8. [Troubleshooting](#troubleshooting)
9. [API Documentation](#api-documentation)
10. [Maintenance & Support](#maintenance--support)

---

## Project Overview

### What is the Resume Parser System?

The Resume Parser is an intelligent, AI-powered document processing platform that automatically extracts structured data from resumes and provides comprehensive talent intelligence. This system combines advanced AI technologies with automated file monitoring to create a seamless workflow for HR professionals and recruitment teams.

### Key Features

#### 🤖 **Dual AI Processing**
- **OpenAI GPT Integration**: Leverages GPT-4 and GPT-3.5-turbo for advanced natural language processing
- **Google Gemini Integration**: Uses Gemini-1.5-flash as an alternative or fallback AI provider
- **Intelligent Fallback**: Automatically switches between providers for maximum reliability

#### 📄 **Multi-Format Document Support**
- **PDF Files**: Direct processing with OCR fallback for scanned documents
- **Microsoft Word**: Both modern (.docx) and legacy (.doc) formats
- **Rich Text Format**: .rtf files with full formatting preservation
- **Plain Text**: .txt files for simple text-based resumes

#### 🔍 **Advanced Search Capabilities**
- **Elasticsearch Integration**: DTSearch-like functionality for powerful document search
- **Boolean Search**: Complex queries with AND, OR, NOT operators
- **Full-Text Search**: Search across all resume content and metadata
- **File Index Search**: Search through any document collection
- **Real-time Suggestions**: Auto-complete and query suggestions

#### 🎯 **QueryMind Integration**
- **Automatic File Monitoring**: Real-time detection of new resume files
- **Smart Classification**: AI-powered identification of CV vs. other documents
- **Seamless Workflow**: Automatic processing and integration with the main system
- **Network Folder Support**: Monitor shared network drives and folders

#### 🌐 **Modern Web Interface**
- **Next.js Frontend**: Fast, responsive React-based user interface
- **Real-time Updates**: Live status updates and progress tracking
- **Batch Processing**: Upload and process multiple resumes simultaneously
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

#### 📊 **Comprehensive Data Extraction**
- **Personal Information**: Name, contact details, location, date of birth
- **Professional Experience**: Work history, current employer, years of experience
- **Skills & Expertise**: Technical skills, soft skills, expertise areas with detailed context
- **Education**: Degrees, certifications, institutions, professional associations
- **Languages**: Language proficiency levels and certifications
- **Industries & Sectors**: Domain experience and industry knowledge
- **Quality Scoring**: Automatic assessment of resume completeness and quality

### System Benefits

#### For HR Professionals
- **Time Savings**: Automated processing eliminates manual data entry
- **Consistency**: Standardized data extraction across all resumes
- **Search Efficiency**: Find candidates quickly using advanced search capabilities
- **Quality Assessment**: Automatic scoring helps prioritize high-quality candidates

#### For IT Administrators
- **Easy Deployment**: Automated setup scripts for quick installation
- **Scalable Architecture**: Supports both small teams and enterprise deployments
- **Flexible Configuration**: Customizable settings for different organizational needs
- **Monitoring Tools**: Built-in diagnostics and health monitoring

#### For Organizations
- **Cost Effective**: Reduces manual processing costs and time
- **Compliance Ready**: Structured data storage for audit and compliance requirements
- **Integration Friendly**: RESTful APIs for integration with existing HR systems
- **Future Proof**: Modern technology stack with regular updates and improvements

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|----------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS | Modern, responsive user interface |
| **Backend** | Django 4.2, Django REST Framework | Robust API and data management |
| **Database** | SQLite (default) / PostgreSQL | Resume data storage and management |
| **Search Engine** | Elasticsearch 7.17 | Advanced search and indexing |
| **AI Processing** | OpenAI GPT, Google Gemini | Intelligent resume parsing |
| **Document Processing** | Unstructured.io, Poppler | Text extraction from various formats |
| **File Monitoring** | Python Watchdog | Real-time file system monitoring |
| **Web Server** | Caddy (production) | High-performance web serving |

### Use Cases

#### 1. **Recruitment Agencies**
- Process hundreds of resumes daily
- Maintain searchable candidate databases
- Quick candidate matching for job requirements

#### 2. **Corporate HR Departments**
- Streamline application processing
- Build internal talent pools
- Compliance and audit trail maintenance

#### 3. **Consulting Firms**
- Manage consultant profiles and expertise
- Quick team assembly for projects
- Skills gap analysis and planning

#### 4. **Educational Institutions**
- Alumni career tracking
- Placement assistance
- Industry partnership management

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 7+ (64-bit), Linux, macOS
- **Python**: 3.10, 3.11, or 3.12 (3.13+ not supported)
- **Node.js**: 16.0 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for installation, additional space for document storage
- **Internet**: Required for AI API calls and package downloads

#### Recommended Requirements
- **RAM**: 16GB for large-scale processing
- **Storage**: SSD for better performance
- **Network**: Stable broadband connection for AI processing
- **Elasticsearch**: For advanced search capabilities (optional but recommended)

### Security & Privacy

#### Data Protection
- **Local Processing**: Resume data stays on your servers
- **API Security**: Secure communication with AI providers
- **Access Control**: User authentication and authorization
- **Audit Logging**: Complete activity tracking

#### Compliance
- **GDPR Ready**: Data protection and privacy controls
- **Configurable Retention**: Automatic data cleanup policies
- **Export Capabilities**: Data portability and backup features

## System Architecture

### Overview

The Resume Parser system follows a modern, microservices-inspired architecture with clear separation of concerns. The system consists of several interconnected components that work together to provide a seamless resume processing experience.

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────────┤
│  Next.js Frontend (Port 3000)                                  │
│  ├── React Components (UI)                                     │
│  ├── TypeScript (Type Safety)                                  │
│  ├── Tailwind CSS (Styling)                                    │
│  └── shadcn/ui (Component Library)                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API GATEWAY LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  Django REST Framework (Port 8000)                             │
│  ├── Authentication & Authorization                            │
│  ├── Request Routing                                           │
│  ├── Response Formatting                                       │
│  └── CORS Handling                                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Django Applications                                            │
│  ├── apps/resumes/     (Resume Management)                     │
│  ├── apps/ai_parser/   (AI Processing)                         │
│  ├── apps/search/      (Search & Indexing)                     │
│  └── apps/core/        (Shared Utilities)                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SERVICE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   AI Services   │  │ Search Services │  │ File Services   │  │
│  │                 │  │                 │  │                 │  │
│  │ • OpenAI GPT    │  │ • Elasticsearch │  │ • Unstructured  │  │
│  │ • Google Gemini │  │ • DTSearch-like │  │ • Document Proc │  │
│  │ • Fallback Logic│  │ • Boolean Search│  │ • Text Extract  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Database      │  │ Search Index    │  │ File Storage    │  │
│  │                 │  │                 │  │                 │  │
│  │ • SQLite/       │  │ • Elasticsearch │  │ • Local Files   │  │
│  │   PostgreSQL    │  │ • Document      │  │ • Media Folder  │  │
│  │ • Resume Data   │  │   Indexing      │  │ • Temp Storage  │  │
│  │ • Metadata      │  │ • Search Cache  │  │ • Uploads       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    QUERYMIND INTEGRATION                        │
├─────────────────────────────────────────────────────────────────┤
│  File Monitoring System                                         │
│  ├── Python Watchdog (Real-time monitoring)                    │
│  ├── Network Folder Support                                    │
│  ├── Automatic CV Detection                                    │
│  └── Integration with Main System                              │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Frontend Layer (Next.js)

**Location**: `frontend/`

**Purpose**: Provides the user interface for the resume parsing system.

**Key Features**:
- **Modern React Framework**: Built with Next.js 14 for optimal performance
- **TypeScript Integration**: Type-safe development with full IntelliSense
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile
- **Component Architecture**: Modular, reusable UI components

**Main Components**:
- `FileUploadZone.tsx` - Drag-and-drop file upload interface
- `ResumeCard.tsx` - Display parsed resume information
- `SearchFilters.tsx` - Advanced search and filtering controls
- `DTSearchPanel.tsx` - DTSearch-like search interface
- `ExpertiseDetailsModal.tsx` - Detailed expertise information display

#### 2. Backend API Layer (Django)

**Location**: `backend/`

**Purpose**: Provides RESTful APIs and handles all business logic.

**Key Features**:
- **Django REST Framework**: Robust API development framework
- **Authentication**: User management and access control
- **File Handling**: Secure file upload and processing
- **Data Validation**: Input validation and sanitization

**Application Structure**:
```
backend/apps/
├── resumes/        # Resume data management
│   ├── models.py    # Resume database model
│   ├── views.py     # API endpoints
│   ├── serializers.py # Data serialization
│   └── admin.py     # Admin interface
├── ai_parser/      # AI processing services
│   ├── services.py  # Main parsing service
│   ├── gemini_service.py # Google Gemini integration
│   ├── unstructured_service.py # Document processing
│   └── doc_converter.py # Document conversion
├── search/         # Search functionality
│   ├── services.py  # Search service
│   ├── documents.py # Elasticsearch mappings
│   ├── views.py     # Search API endpoints
│   └── tasks.py     # Background indexing
└── core/           # Shared utilities
    ├── views.py     # Common API views
    └── urls.py      # URL routing
```

#### 3. AI Processing Layer

**Purpose**: Handles intelligent resume parsing using multiple AI providers.

**Components**:

**OpenAI Integration**:
- **Models**: GPT-4, GPT-3.5-turbo, GPT-4o-mini
- **Features**: Advanced natural language understanding
- **Fallback**: Automatic model switching on errors

**Google Gemini Integration**:
- **Models**: Gemini-1.5-flash, Gemini-1.5-pro
- **Features**: Fast processing, cost-effective
- **Backup**: Primary or secondary AI provider

**Processing Pipeline**:
1. **Text Extraction**: Unstructured.io processes documents
2. **AI Analysis**: Structured data extraction using AI
3. **Data Validation**: Quality checks and data cleaning
4. **Storage**: Parsed data saved to database
5. **Indexing**: Content indexed for search

#### 4. Document Processing Layer

**Purpose**: Extracts text from various document formats.

**Technologies**:
- **Unstructured.io**: Advanced document processing library
- **Poppler**: PDF text extraction and rendering
- **Python-docx**: Microsoft Word document processing
- **PyPDF**: PDF text extraction

**Supported Formats**:
- **PDF**: Direct text extraction with OCR fallback
- **DOCX**: Modern Word documents with formatting
- **DOC**: Legacy Word documents
- **RTF**: Rich Text Format documents
- **TXT**: Plain text files

#### 5. Search Layer (Elasticsearch)

**Purpose**: Provides advanced search capabilities similar to DTSearch.

**Features**:
- **Full-Text Search**: Search across all resume content
- **Boolean Queries**: Complex search with AND, OR, NOT operators
- **Faceted Search**: Filter by skills, experience, location, etc.
- **Auto-complete**: Real-time search suggestions
- **Highlighting**: Search term highlighting in results

**Index Structure**:
```json
{
  "cv_documents": {
    "mappings": {
      "properties": {
        "content": {"type": "text", "analyzer": "standard"},
        "name": {"type": "text", "analyzer": "standard"},
        "skills": {"type": "keyword"},
        "experience_years": {"type": "integer"},
        "location": {"type": "keyword"},
        "file_type": {"type": "keyword"},
        "timestamp": {"type": "date"}
      }
    }
  }
}
```

#### 6. QueryMind Integration Layer

**Purpose**: Provides automatic file monitoring and CV detection.

**Components**:

**File Watcher** (`file_watcher.py`):
- **Real-time Monitoring**: Watches specified folders for new files
- **Event Handling**: Processes file creation, modification, and move events
- **Smart Filtering**: Only processes relevant file types
- **Debouncing**: Prevents duplicate processing

**Integration Manager** (`integration_manager.py`):
- **Configuration Management**: Enable/disable integration
- **Connection Testing**: Verify backend connectivity
- **Status Monitoring**: Track integration health

**Main Processing** (`main.py`):
- **CV Classification**: AI-powered document classification
- **Automatic Upload**: Sends detected CVs to main system
- **Statistics Tracking**: Monitor processing success rates

### Data Flow

#### 1. Manual Upload Flow
```
User Upload → Frontend → API Gateway → File Validation → 
Text Extraction → AI Processing → Data Storage → Search Indexing
```

#### 2. QueryMind Automatic Flow
```
File Detection → CV Classification → Automatic Upload → 
API Processing → Data Storage → Search Indexing
```

#### 3. Search Flow
```
Search Query → Frontend → API Gateway → Elasticsearch → 
Result Formatting → Frontend Display
```

### Database Schema

#### Resume Model
```sql
CREATE TABLE resumes_resume (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    cv_hash VARCHAR(64) UNIQUE,
    content_hash VARCHAR(64),
    person_soft_id VARCHAR(64),
    
    -- Personal Information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(254),
    phone_number VARCHAR(20),
    location VARCHAR(200),
    date_of_birth DATE,
    
    -- Professional Information
    current_employer VARCHAR(200),
    years_of_experience INTEGER,
    total_experience_months INTEGER,
    availability VARCHAR(100),
    
    -- Skills and Expertise (JSON)
    expertise_areas TEXT,
    expertise_details TEXT,
    sectors TEXT,
    skill_keywords TEXT,
    
    -- File Information
    original_filename VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(10),
    
    -- Processing Status
    is_processed BOOLEAN DEFAULT FALSE,
    processing_status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT
);
```

### Security Architecture

#### Authentication & Authorization
- **Django Authentication**: Built-in user management
- **Session Management**: Secure session handling
- **CORS Configuration**: Cross-origin request security
- **API Rate Limiting**: Prevent abuse and overload

#### Data Security
- **Input Validation**: All inputs validated and sanitized
- **File Type Validation**: Only allowed file types processed
- **Secure File Storage**: Files stored in protected directories
- **API Key Management**: Secure storage of AI provider keys

#### Network Security
- **HTTPS Support**: SSL/TLS encryption in production
- **Firewall Configuration**: Network access controls
- **Internal Communication**: Secure inter-service communication

## Installation and Setup

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 2 GB free space for application, additional space for resume files
- **Network**: Internet connection for AI services and package downloads

#### Software Dependencies
- **Python**: 3.10, 3.11, or 3.12
- **Node.js**: Version 16 or higher
- **npm**: Version 8 or higher (comes with Node.js)
- **Git**: For cloning the repository

#### Optional Dependencies
- **Elasticsearch**: For advanced search functionality (can be installed separately)
- **PostgreSQL**: For production database (SQLite used by default)
- **Poppler**: For enhanced PDF processing

### Quick Start (Portable Version)

For users who want to get started quickly without manual setup:

1. **Download the portable version** (if available)
2. **Extract** the archive to your desired location
3. **Run** `START_RESUME_PARSER.bat` (Windows) or `start_resume_parser.sh` (Linux/Mac)
4. **Configure API keys** when prompted
5. **Access** the application at `http://localhost:3000`

### Manual Installation

#### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd resume-parser

# Or download and extract the ZIP file
```

#### Step 2: Backend Setup (Django)

##### 2.1 Navigate to Backend Directory
```bash
cd backend
```

##### 2.2 Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

##### 2.3 Install Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# For production deployment
pip install -r production_requirements.txt
```

##### 2.4 Install System Dependencies

**Windows:**
```cmd
# Install Poppler for PDF processing
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Extract and add to PATH
```

**macOS:**
```bash
# Using Homebrew
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

##### 2.5 Configure Environment Variables

Create a `.env` file in the backend directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL (production)
# DATABASE_URL=postgresql://username:password@localhost:5432/resume_parser

# AI Provider Settings
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-gemini-api-key

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=pdf,doc,docx,rtf,txt

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# Elasticsearch (optional)
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX=cv_documents
```

##### 2.6 Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

##### 2.7 Test Backend Installation
```bash
# Start development server
python manage.py runserver

# Server should start at http://127.0.0.1:8000
# Test API at http://127.0.0.1:8000/api/
```

#### Step 3: Frontend Setup (Next.js)

##### 3.1 Navigate to Frontend Directory
```bash
cd ../frontend
```

##### 3.2 Install Node.js Dependencies
```bash
# Install packages
npm install

# Or using yarn
yarn install
```

##### 3.3 Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Analytics or other services
# NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

##### 3.4 Test Frontend Installation
```bash
# Start development server
npm run dev

# Or using yarn
yarn dev

# Server should start at http://localhost:3000
```

#### Step 4: Verify Installation

1. **Backend Check**: Visit `http://localhost:8000/admin` and log in with your admin credentials
2. **Frontend Check**: Visit `http://localhost:3000` and verify the upload interface loads
3. **API Check**: Visit `http://localhost:8000/api/resumes/` to see the API response
4. **Upload Test**: Try uploading a sample resume file

### AI Provider Configuration

#### OpenAI Setup

1. **Create Account**: Visit [OpenAI Platform](https://platform.openai.com)
2. **Generate API Key**: Go to API Keys section and create a new key
3. **Add to Environment**: Set `OPENAI_API_KEY` in your `.env` file
4. **Configure Models**: Available models:
   - `gpt-4` (highest quality, slower)
   - `gpt-3.5-turbo` (balanced performance)
   - `gpt-4o-mini` (fastest, cost-effective)

#### Google Gemini Setup

1. **Create Project**: Visit [Google AI Studio](https://aistudio.google.com)
2. **Generate API Key**: Create a new API key for your project
3. **Add to Environment**: Set `GOOGLE_API_KEY` in your `.env` file
4. **Configure Models**: Available models:
   - `gemini-1.5-pro` (highest quality)
   - `gemini-1.5-flash` (faster processing)

#### AI Provider Priority

The system can use both providers with automatic fallback:

```python
# In backend/settings.py
AI_PROVIDERS = {
    'primary': 'openai',    # or 'gemini'
    'fallback': 'gemini',   # or 'openai'
    'models': {
        'openai': 'gpt-3.5-turbo',
        'gemini': 'gemini-1.5-flash'
    }
}
```

### Elasticsearch Setup (Optional)

For advanced search functionality:

#### Installation

**Docker (Recommended):**
```bash
# Pull and run Elasticsearch
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.11.0
```

**Manual Installation:**
1. Download from [Elastic.co](https://www.elastic.co/downloads/elasticsearch)
2. Extract and run according to platform instructions
3. Verify at `http://localhost:9200`

#### Configuration

Add to your backend `.env` file:
```env
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX=cv_documents
ELASTICSEARCH_ENABLED=True
```

#### Index Creation
```bash
# Create search index
python manage.py shell

# In Python shell:
from apps.search.services import SearchService
search_service = SearchService()
search_service.create_index()
```

### Production Deployment

#### Using Production Scripts

The project includes production deployment scripts:

**Windows:**
```cmd
# Install production dependencies
pip install -r production_requirements.txt

# Start production server
start_production.bat
```

**Linux/macOS:**
```bash
# Install production dependencies
pip install -r production_requirements.txt

# Start production server
./start_production.sh
```

#### Manual Production Setup

##### Backend (Django)
```bash
# Install production server
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

##### Frontend (Next.js)
```bash
# Build for production
npm run build

# Start production server
npm start
```

##### Reverse Proxy (Caddy)

The project includes a `Caddyfile` for easy reverse proxy setup:

```caddyfile
localhost {
    handle /api/* {
        reverse_proxy localhost:8000
    }
    handle /admin/* {
        reverse_proxy localhost:8000
    }
    handle /static/* {
        reverse_proxy localhost:8000
    }
    handle {
        reverse_proxy localhost:3000
    }
}
```

### Configuration Options

#### File Upload Settings

```python
# In backend/settings.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10MB

# Allowed file types
ALLOWED_FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.rtf', '.txt']

# Upload directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

#### AI Processing Settings

```python
# AI provider configuration
AI_CONFIG = {
    'timeout': 30,  # seconds
    'max_retries': 3,
    'chunk_size': 4000,  # characters
    'temperature': 0.1,  # AI creativity (0-1)
}
```

#### Search Configuration

```python
# Elasticsearch settings
SEARCH_CONFIG = {
    'index_name': 'cv_documents',
    'max_results': 100,
    'highlight_fragments': 3,
    'cache_timeout': 300,  # seconds
}
```

### Verification and Testing

#### Health Checks

1. **Backend Health**: `http://localhost:8000/api/health/`
2. **Frontend Health**: `http://localhost:3000/api/health`
3. **Database**: Check admin panel at `http://localhost:8000/admin/`
4. **AI Services**: Upload a test resume and verify parsing

#### Test Resume Upload

1. Navigate to `http://localhost:3000`
2. Drag and drop a sample resume (PDF, DOCX, etc.)
3. Verify the file uploads successfully
4. Check that AI parsing completes
5. Verify data appears in the admin panel

#### Performance Testing

```bash
# Test API performance
curl -X GET "http://localhost:8000/api/resumes/" \
     -H "Accept: application/json" \
     -w "@curl-format.txt"

# Test file upload
curl -X POST "http://localhost:8000/api/resumes/upload/" \
     -F "file=@sample_resume.pdf" \
     -w "@curl-format.txt"
```

## QueryMind Integration

### Overview

QueryMind is an intelligent file monitoring system that automatically detects and processes resume files from specified directories. This integration enables hands-free operation where the system continuously monitors folders (including network drives) for new CV files and automatically processes them through the main Resume Parser system.

### Key Features

- **Real-time File Monitoring**: Uses Python Watchdog for instant file detection
- **AI-Powered CV Classification**: Automatically identifies resume files vs. other documents
- **Network Folder Support**: Monitor shared drives and network locations
- **Automatic Processing**: Seamless integration with the main parsing system
- **Duplicate Prevention**: Smart hash-based duplicate detection
- **Statistics Tracking**: Monitor processing success rates and performance
- **Configurable Filtering**: Customize file types and folder exclusions

### System Requirements

#### Software Requirements
- **Python**: 3.10+ (same as main system)
- **Main Resume Parser**: Must be running and accessible
- **Network Access**: For monitoring network drives (if applicable)

#### Hardware Requirements
- **RAM**: Additional 512MB for file monitoring
- **Storage**: Minimal (logs and temporary files)
- **Network**: Stable connection to monitored folders

### Installation and Setup

#### Step 1: Verify Main System

Ensure the main Resume Parser system is installed and running:

```bash
# Test backend connectivity
curl http://localhost:8000/api/health/

# Should return: {"status": "healthy"}
```

#### Step 2: Configure QueryMind

Navigate to the QueryMind directory and edit the configuration:

```bash
cd QueryMind
```

Edit `main.py` to configure your settings:

```python
# QueryMind Configuration
SOURCE_FOLDER = r"C:\Users\YourName\Documents\CVs"  # Folder to monitor
RESUME_PARSER_URL = "http://localhost:8000"         # Backend URL
INTEGRATION_ENABLED = True                          # Enable/disable integration

# Advanced Settings
MONITOR_SUBDIRECTORIES = True                       # Monitor subfolders
FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.rtf', '.txt']  # Allowed types
DEBOUNCE_SECONDS = 2                               # Wait time for file stability
MAX_FILE_SIZE_MB = 10                              # Maximum file size

# AI Classification Settings
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.7          # CV detection confidence
USE_AI_CLASSIFICATION = True                       # Enable AI-based detection

# Logging Configuration
LOG_LEVEL = "INFO"                                  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "querymind.log"                         # Log file name
MAX_LOG_SIZE_MB = 50                               # Log rotation size
```

#### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Key dependencies:
# - watchdog (file monitoring)
# - requests (HTTP communication)
# - openai (AI classification)
# - python-magic (file type detection)
```

#### Step 4: Test Configuration

```bash
# Test the integration setup
python integration_manager.py --test

# Expected output:
# ✓ Source folder exists and is accessible
# ✓ Resume Parser backend is reachable
# ✓ AI classification is working
# ✓ Integration is properly configured
```

### Configuration Options

#### Basic Configuration

**Source Folder Setup:**
```python
# Local folder
SOURCE_FOLDER = r"C:\CVs\Incoming"

# Network drive (Windows)
SOURCE_FOLDER = r"\\server\shared\CVs"

# Network drive (mapped)
SOURCE_FOLDER = r"Z:\CVs"

# Multiple folders (advanced)
SOURCE_FOLDERS = [
    r"C:\CVs\Incoming",
    r"\\server\shared\CVs",
    r"C:\Users\HR\Desktop\Resumes"
]
```

**File Filtering:**
```python
# File type filtering
FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.rtf', '.txt']

# Size limits
MIN_FILE_SIZE_KB = 1      # Minimum file size
MAX_FILE_SIZE_MB = 10     # Maximum file size

# Exclude patterns
EXCLUDE_PATTERNS = [
    '*temp*',              # Temporary files
    '*~*',                 # Backup files
    '*.tmp',               # Temporary extensions
    '*draft*'              # Draft documents
]

# Include only specific patterns
INCLUDE_PATTERNS = [
    '*resume*',
    '*cv*',
    '*curriculum*'
]
```

#### Advanced Configuration

**AI Classification Settings:**
```python
# OpenAI configuration for CV detection
AI_CLASSIFICATION = {
    'enabled': True,
    'api_key': 'your-openai-api-key',
    'model': 'gpt-3.5-turbo',
    'confidence_threshold': 0.7,
    'max_text_length': 2000,  # Characters to analyze
    'timeout': 10             # Seconds
}

# Classification prompt
CLASSIFICATION_PROMPT = """
Analyze this document text and determine if it's a resume/CV.
Respond with only 'YES' or 'NO' followed by confidence (0-1).
Example: 'YES 0.95' or 'NO 0.80'

Document text:
{text}
"""
```

**Performance Tuning:**
```python
# File processing settings
PROCESSING_CONFIG = {
    'debounce_seconds': 2,        # Wait for file stability
    'max_concurrent_files': 3,   # Parallel processing limit
    'retry_attempts': 3,         # Failed upload retries
    'retry_delay': 5,            # Seconds between retries
    'batch_size': 10,            # Files per batch
    'queue_max_size': 100        # Maximum queue size
}

# Monitoring settings
MONITORING_CONFIG = {
    'check_interval': 1,         # Seconds between checks
    'health_check_interval': 60, # Backend health checks
    'statistics_interval': 300,  # Stats logging interval
    'cleanup_interval': 3600     # Cleanup old logs/temp files
}
```

### Running QueryMind

#### Manual Start

```bash
# Start file monitoring
python main.py

# With verbose logging
python main.py --verbose

# With custom config
python main.py --config custom_config.py
```

#### Service Mode (Windows)

Create a Windows service for automatic startup:

```bash
# Install as Windows service
python service_installer.py install

# Start the service
net start QueryMindService

# Stop the service
net stop QueryMindService

# Remove the service
python service_installer.py remove
```

#### Service Mode (Linux/macOS)

Create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/querymind.service
```

```ini
[Unit]
Description=QueryMind Resume File Monitor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/QueryMind
ExecStart=/path/to/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable querymind
sudo systemctl start querymind

# Check status
sudo systemctl status querymind
```

### Management and Monitoring

#### Integration Manager

Use the integration manager for system control:

```bash
# Check integration status
python integration_manager.py --status

# Enable integration
python integration_manager.py --enable

# Disable integration
python integration_manager.py --disable

# Test all components
python integration_manager.py --test

# Reset configuration
python integration_manager.py --reset
```

#### Real-time Monitoring

**View Live Logs:**
```bash
# Follow log file
tail -f querymind.log

# Filter for specific events
tail -f querymind.log | grep "CV detected"

# View errors only
tail -f querymind.log | grep "ERROR"
```

**Statistics Dashboard:**
```bash
# View processing statistics
python stats_viewer.py

# Output example:
# QueryMind Statistics (Last 24 hours)
# =====================================
# Files Detected: 45
# CVs Identified: 32
# Successfully Processed: 30
# Duplicates Skipped: 8
# Errors: 2
# Success Rate: 93.75%
```

#### Web Interface Integration

QueryMind status is displayed in the main web interface:

1. **Dashboard Widget**: Shows monitoring status and recent activity
2. **Statistics Panel**: Displays processing metrics
3. **Configuration Panel**: Allows basic settings changes
4. **Log Viewer**: Browse recent log entries

### File Processing Workflow

#### 1. File Detection
```
File Event → File Validation → Size/Type Check → Stability Wait
```

#### 2. CV Classification
```
Text Extraction → AI Analysis → Confidence Check → Classification Decision
```

#### 3. Processing Pipeline
```
CV Confirmed → Duplicate Check → Upload to Backend → Processing Status
```

#### 4. Error Handling
```
Error Detected → Retry Logic → Fallback Options → Error Logging
```

### Troubleshooting

#### Common Issues

**1. Files Not Being Detected**
```bash
# Check folder permissions
ls -la /path/to/source/folder

# Verify folder monitoring
python -c "import os; print(os.path.exists('SOURCE_FOLDER'))"

# Test file events
python test_file_events.py
```

**2. Backend Connection Issues**
```bash
# Test backend connectivity
curl http://localhost:8000/api/health/

# Check network configuration
ping localhost

# Verify firewall settings
telnet localhost 8000
```

**3. AI Classification Errors**
```bash
# Test OpenAI API key
python test_ai_classification.py

# Check API quota
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.openai.com/v1/usage

# Verify text extraction
python test_text_extraction.py sample.pdf
```

**4. Performance Issues**
```bash
# Monitor system resources
top -p $(pgrep -f "python main.py")

# Check disk space
df -h

# Monitor network usage
netstat -i
```

#### Debug Mode

Enable detailed debugging:

```python
# In main.py
LOG_LEVEL = "DEBUG"
DEBUG_MODE = True
VERBOSE_LOGGING = True

# Additional debug options
DEBUG_CONFIG = {
    'log_file_events': True,
    'log_ai_responses': True,
    'log_api_calls': True,
    'save_extracted_text': True,
    'preserve_temp_files': True
}
```

#### Log Analysis

**Common Log Patterns:**
```bash
# Successful processing
grep "Successfully uploaded" querymind.log

# Classification results
grep "CV classification" querymind.log

# Error patterns
grep -E "ERROR|CRITICAL" querymind.log

# Performance metrics
grep "Processing time" querymind.log
```

### Security Considerations

#### File Access Security
- **Folder Permissions**: Ensure appropriate read access to monitored folders
- **Network Security**: Use secure network protocols for remote folders
- **File Validation**: Validate file types and sizes before processing

#### API Security
- **API Key Protection**: Store OpenAI keys securely
- **Backend Authentication**: Use secure communication with the main system
- **Rate Limiting**: Implement appropriate API usage limits

#### Data Privacy
- **Temporary Files**: Automatically clean up extracted text
- **Log Sanitization**: Avoid logging sensitive information
- **Access Logging**: Track file access for audit purposes

## Web Interface Usage Guide

### Overview

The Resume Parser web interface provides an intuitive, modern interface for uploading, processing, and managing resume data. Built with Next.js and React, it offers a responsive design that works seamlessly across desktop, tablet, and mobile devices.

### Accessing the Application

#### Development Environment
- **Frontend**: `http://localhost:3000`
- **Backend Admin**: `http://localhost:8000/admin`
- **API Documentation**: `http://localhost:8000/api/`

#### Production Environment
- **Main Application**: `https://your-domain.com`
- **Admin Panel**: `https://your-domain.com/admin`

### Main Dashboard

#### Dashboard Overview

The main dashboard provides a comprehensive view of your resume processing system:

**Key Elements:**
- **Upload Zone**: Central file upload area with drag-and-drop functionality
- **Recent Uploads**: List of recently processed resumes
- **Statistics Panel**: Processing metrics and system status
- **Search Bar**: Quick search across all resumes
- **Navigation Menu**: Access to different sections

**Dashboard Widgets:**
1. **Total Resumes**: Count of all processed resumes
2. **Processing Status**: Current system activity
3. **Success Rate**: Percentage of successful processing
4. **Storage Usage**: Disk space utilization
5. **QueryMind Status**: File monitoring system status

#### Navigation Structure

```
Main Dashboard
├── Upload
│   ├── Single File Upload
│   ├── Batch Upload
│   └── Upload History
├── Browse Resumes
│   ├── Resume List
│   ├── Detailed View
│   └── Export Options
├── Search
│   ├── Basic Search
│   ├── Advanced Filters
│   └── DTSearch Panel
├── Analytics
│   ├── Processing Statistics
│   ├── Performance Metrics
│   └── Usage Reports
└── Settings
    ├── AI Configuration
    ├── File Settings
    └── System Preferences
```

### File Upload Process

#### Single File Upload

**Step 1: Access Upload Area**
1. Navigate to the main dashboard
2. Locate the central upload zone
3. The area displays "Drag and drop files here or click to browse"

**Step 2: Select File**

*Method 1 - Drag and Drop:*
1. Open your file manager
2. Navigate to the resume file
3. Drag the file to the upload zone
4. Drop when the zone highlights

*Method 2 - File Browser:*
1. Click on the upload zone
2. File browser dialog opens
3. Navigate to your resume file
4. Select the file and click "Open"

**Step 3: File Validation**
- System validates file type (PDF, DOC, DOCX, RTF, TXT)
- Checks file size (maximum 10MB by default)
- Displays validation status with green checkmark or red error

**Step 4: Processing**
1. Upload progress bar appears
2. File is uploaded to the server
3. Text extraction begins
4. AI processing starts
5. Progress indicators show each stage

**Step 5: Results**
- Processing completion notification
- Parsed data preview
- Option to view full details
- Success/error status display

#### Batch Upload

**Accessing Batch Upload:**
1. Click "Batch Upload" button on dashboard
2. Or navigate to Upload → Batch Upload

**Batch Upload Process:**
1. **Select Multiple Files**: Choose up to 20 files simultaneously
2. **Queue Management**: Files are queued for processing
3. **Progress Tracking**: Individual progress for each file
4. **Batch Status**: Overall batch completion status
5. **Results Summary**: Success/failure count and details

**Batch Upload Features:**
- **Parallel Processing**: Multiple files processed simultaneously
- **Error Handling**: Failed files can be retried individually
- **Progress Indicators**: Real-time status for each file
- **Cancellation**: Stop processing at any time
- **Results Export**: Download batch processing results

### Resume Management

#### Resume List View

**Accessing Resume List:**
- Click "Browse Resumes" in the main navigation
- Or use the "View All" link from the dashboard

**List Features:**

**Column Layout:**
- **Name**: Candidate's full name (clickable for details)
- **Email**: Contact email address
- **Phone**: Phone number
- **Experience**: Years of experience
- **Skills**: Key skills preview
- **Upload Date**: When the resume was processed
- **Status**: Processing status indicator
- **Actions**: View, Edit, Delete, Export options

**Sorting Options:**
- **Name**: Alphabetical order
- **Date**: Most recent first
- **Experience**: Years of experience
- **Relevance**: Search relevance score

**Filtering Options:**
- **Experience Level**: Junior, Mid-level, Senior
- **Skills**: Filter by specific skills
- **Location**: Geographic location
- **Upload Date**: Date range selection
- **File Type**: PDF, DOC, DOCX, etc.

#### Detailed Resume View

**Accessing Details:**
1. Click on any resume name in the list
2. Or click the "View" button in the actions column

**Detail Sections:**

**1. Personal Information**
```
┌─────────────────────────────────────┐
│ Personal Information                │
├─────────────────────────────────────┤
│ Name: John Smith                    │
│ Email: john.smith@email.com         │
│ Phone: +1 (555) 123-4567           │
│ Location: New York, NY              │
│ Date of Birth: 1990-05-15          │
└─────────────────────────────────────┘
```

**2. Professional Summary**
```
┌─────────────────────────────────────┐
│ Professional Information            │
├─────────────────────────────────────┤
│ Current Employer: Tech Corp         │
│ Years of Experience: 8              │
│ Total Experience: 96 months         │
│ Availability: Immediate             │
└─────────────────────────────────────┘
```

**3. Skills and Expertise**
```
┌─────────────────────────────────────┐
│ Skills & Expertise                  │
├─────────────────────────────────────┤
│ Technical Skills:                   │
│ • Python, JavaScript, React        │
│ • AWS, Docker, Kubernetes          │
│ • Machine Learning, AI              │
│                                     │
│ Expertise Areas:                    │
│ • Software Development             │
│ • Cloud Architecture               │
│ • Team Leadership                  │
│                                     │
│ Industry Sectors:                   │
│ • Technology                       │
│ • Financial Services               │
│ • Healthcare                       │
└─────────────────────────────────────┘
```

**4. Education and Certifications**
- Educational background
- Degrees and institutions
- Professional certifications
- Training and courses

**5. Work History**
- Employment timeline
- Company names and positions
- Job descriptions and achievements
- Career progression

**6. Languages**
- Spoken languages
- Proficiency levels
- Native/fluent/conversational

#### Resume Actions

**Available Actions:**

**1. Edit Resume**
- Click "Edit" button
- Modify any field
- Save changes
- View edit history

**2. Export Resume**
- **PDF Export**: Formatted resume document
- **JSON Export**: Structured data format
- **CSV Export**: Spreadsheet-compatible format
- **XML Export**: Structured markup format

**3. Delete Resume**
- Click "Delete" button
- Confirmation dialog appears
- Permanent deletion (cannot be undone)
- Option to archive instead

**4. Duplicate Resume**
- Create a copy for editing
- Useful for similar candidates
- Maintains original data

**5. Share Resume**
- Generate shareable link
- Set access permissions
- Time-limited access
- Password protection option

### Search Functionality

#### Basic Search

**Search Bar Location:**
- Top of every page
- Prominent position in header
- Always accessible

**Search Process:**
1. **Enter Query**: Type search terms in the search bar
2. **Auto-suggestions**: Real-time suggestions appear
3. **Execute Search**: Press Enter or click search icon
4. **View Results**: Results displayed with relevance ranking

**Search Capabilities:**
- **Full-text Search**: Search across all resume content
- **Partial Matching**: Find partial words and phrases
- **Fuzzy Search**: Handle typos and variations
- **Stemming**: Find word variations (develop, developer, development)

#### Advanced Search

**Accessing Advanced Search:**
1. Click "Advanced Search" link near search bar
2. Or navigate to Search → Advanced Filters

**Advanced Search Fields:**

**Personal Information:**
- Name (first, last, full)
- Email domain
- Phone area code
- Location (city, state, country)
- Age range

**Professional Criteria:**
- Current employer
- Previous employers
- Job titles
- Years of experience (range)
- Salary expectations
- Availability

**Skills and Expertise:**
- Technical skills (exact match)
- Skill categories
- Expertise areas
- Industry sectors
- Certifications

**Education:**
- Degree level
- Field of study
- Institution name
- Graduation year

**File Metadata:**
- Upload date range
- File type
- File size
- Processing status

#### Search Results

**Results Layout:**

**List View:**
```
┌─────────────────────────────────────────────────────────┐
│ Search Results (24 found)                               │
├─────────────────────────────────────────────────────────┤
│ [★★★★☆] John Smith - Senior Developer                  │
│ 8 years exp | Python, React, AWS | New York, NY       │
│ Highlights: "Python developer with React experience"   │
│ ─────────────────────────────────────────────────────── │
│ [★★★☆☆] Jane Doe - Software Engineer                   │
│ 5 years exp | Java, Spring, Docker | San Francisco    │
│ Highlights: "Full-stack developer with cloud exp"     │
└─────────────────────────────────────────────────────────┘
```

**Card View:**
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ John Smith      │ │ Jane Doe        │ │ Mike Johnson    │
│ Senior Dev      │ │ Software Eng    │ │ Tech Lead       │
│ ★★★★☆          │ │ ★★★☆☆          │ │ ★★★★★          │
│ 8 yrs | Python │ │ 5 yrs | Java    │ │ 10 yrs | C++    │
│ New York, NY    │ │ San Francisco   │ │ Seattle, WA     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Result Features:**
- **Relevance Score**: Star rating (1-5 stars)
- **Highlighted Terms**: Search terms highlighted in results
- **Quick Preview**: Key information at a glance
- **Action Buttons**: View, Contact, Save, Export

#### Search Filters

**Filter Panel:**
Located on the left side of search results

**Available Filters:**

**Experience Level:**
- ☐ Entry Level (0-2 years)
- ☐ Mid-Level (3-7 years)
- ☐ Senior (8-15 years)
- ☐ Executive (15+ years)

**Skills Categories:**
- ☐ Programming Languages
- ☐ Web Development
- ☐ Mobile Development
- ☐ Data Science
- ☐ DevOps
- ☐ Design
- ☐ Management

**Location:**
- ☐ Remote
- ☐ United States
- ☐ Europe
- ☐ Asia
- ☐ Other

**Education:**
- ☐ High School
- ☐ Bachelor's Degree
- ☐ Master's Degree
- ☐ PhD
- ☐ Professional Certification

**File Type:**
- ☐ PDF
- ☐ DOC/DOCX
- ☐ RTF
- ☐ TXT

### DTSearch Integration

#### DTSearch Panel

**Accessing DTSearch:**
1. Click "DTSearch" tab in the search interface
2. Or navigate to Search → DTSearch Panel

**DTSearch Features:**

**Boolean Search:**
```
┌─────────────────────────────────────────────────────────┐
│ DTSearch Query Builder                                  │
├─────────────────────────────────────────────────────────┤
│ Query: [Python AND (React OR Angular) NOT Java]        │
│                                                         │
│ ☐ Case Sensitive    ☐ Whole Words Only                │
│ ☐ Fuzzy Search      ☐ Stemming                        │
│                                                         │
│ [Search] [Clear] [Save Query] [Load Query]             │
└─────────────────────────────────────────────────────────┘
```

**Query Operators:**
- **AND**: Both terms must be present
- **OR**: Either term can be present
- **NOT**: Exclude documents with this term
- **NEAR**: Terms must be within specified distance
- **Wildcards**: Use * for partial matching
- **Phrases**: Use quotes for exact phrases

**Example Queries:**
```
# Find Python developers with React experience
Python AND React

# Find senior developers (excluding junior)
"senior developer" NOT junior

# Find full-stack developers
"full stack" OR "full-stack" OR (frontend AND backend)

# Find developers in specific locations
("New York" OR "San Francisco" OR "Seattle") AND developer

# Find experienced developers with specific skills
(Python OR Java OR JavaScript) AND (5+ OR "5 years" OR senior)
```

#### Advanced DTSearch Features

**Field-Specific Search:**
```
name:John AND skills:Python
email:@gmail.com AND experience:>5
location:"New York" AND title:"Senior"
```

**Date Range Search:**
```
upload_date:[2024-01-01 TO 2024-12-31]
graduation_year:[2015 TO 2020]
```

**Numeric Range Search:**
```
experience:[5 TO 10]
salary:[80000 TO 120000]
age:[25 TO 35]
```

### Analytics and Reporting

#### Processing Statistics

**Statistics Dashboard:**

**Overview Metrics:**
```
┌─────────────────────────────────────────────────────────┐
│ Processing Statistics (Last 30 Days)                   │
├─────────────────────────────────────────────────────────┤
│ Total Resumes Processed: 1,247                         │
│ Success Rate: 94.2%                                    │
│ Average Processing Time: 12.3 seconds                  │
│ Failed Uploads: 72 (5.8%)                             │
│ Duplicate Resumes: 23 (1.8%)                          │
└─────────────────────────────────────────────────────────┘
```

**Processing Breakdown:**
- **By File Type**: PDF (65%), DOCX (25%), DOC (8%), Other (2%)
- **By AI Provider**: OpenAI (70%), Gemini (30%)
- **By Source**: Manual Upload (60%), QueryMind (40%)
- **By Time**: Peak hours, daily patterns

**Performance Metrics:**
- **Average Processing Time**: Per file type and size
- **Success Rates**: By AI provider and file type
- **Error Analysis**: Common failure reasons
- **Resource Usage**: CPU, memory, storage

#### Usage Reports

**Report Types:**

**1. Daily Activity Report**
- Uploads per day
- Processing success/failure rates
- Peak usage times
- User activity patterns

**2. Weekly Summary**
- Total resumes processed
- Quality metrics
- System performance
- Error trends

**3. Monthly Analytics**
- Growth trends
- Capacity planning data
- Cost analysis
- ROI metrics

**4. Custom Reports**
- Date range selection
- Metric customization
- Export formats (PDF, Excel, CSV)
- Scheduled delivery

### Settings and Configuration

#### AI Provider Settings

**Accessing AI Settings:**
1. Navigate to Settings → AI Configuration
2. Or click the gear icon in the header

**OpenAI Configuration:**
```
┌─────────────────────────────────────────────────────────┐
│ OpenAI Settings                                         │
├─────────────────────────────────────────────────────────┤
│ API Key: [••••••••••••••••••••••••••••••••••••••••••] │
│ Model: [gpt-3.5-turbo ▼]                               │
│ Temperature: [0.1] (0.0 - 1.0)                        │
│ Max Tokens: [4000]                                     │
│ Timeout: [30] seconds                                  │
│                                                         │
│ ☑ Enable as Primary Provider                           │
│ ☑ Enable Fallback to Gemini                           │
│                                                         │
│ [Test Connection] [Save Settings]                      │
└─────────────────────────────────────────────────────────┘
```

**Google Gemini Configuration:**
```
┌─────────────────────────────────────────────────────────┐
│ Google Gemini Settings                                  │
├─────────────────────────────────────────────────────────┤
│ API Key: [••••••••••••••••••••••••••••••••••••••••••] │
│ Model: [gemini-1.5-flash ▼]                           │
│ Temperature: [0.1] (0.0 - 1.0)                        │
│ Max Tokens: [4000]                                     │
│ Timeout: [30] seconds                                  │
│                                                         │
│ ☐ Enable as Primary Provider                           │
│ ☑ Enable as Fallback Provider                         │
│                                                         │
│ [Test Connection] [Save Settings]                      │
└─────────────────────────────────────────────────────────┘
```

#### File Upload Settings

**Upload Configuration:**
```
┌─────────────────────────────────────────────────────────┐
│ File Upload Settings                                    │
├─────────────────────────────────────────────────────────┤
│ Maximum File Size: [10] MB                             │
│ Allowed File Types:                                     │
│ ☑ PDF  ☑ DOC  ☑ DOCX  ☑ RTF  ☑ TXT                   │
│                                                         │
│ Upload Directory: [/uploads/resumes/]                  │
│ Temporary Directory: [/tmp/processing/]                │
│                                                         │
│ ☑ Enable Virus Scanning                               │
│ ☑ Enable Duplicate Detection                           │
│ ☑ Auto-delete Failed Uploads                          │
│                                                         │
│ Retention Policy:                                       │
│ Keep Original Files: [Forever ▼]                      │
│ Keep Processed Data: [Forever ▼]                      │
│                                                         │
│ [Save Settings]                                        │
└─────────────────────────────────────────────────────────┘
```

#### System Preferences

**General Settings:**
```
┌─────────────────────────────────────────────────────────┐
│ System Preferences                                      │
├─────────────────────────────────────────────────────────┤
│ Application Name: [Resume Parser]                      │
│ Default Language: [English ▼]                         │
│ Timezone: [UTC-5 (Eastern) ▼]                         │
│ Date Format: [MM/DD/YYYY ▼]                           │
│                                                         │
│ Results Per Page: [25 ▼]                              │
│ Default Sort Order: [Date (Newest First) ▼]           │
│                                                         │
│ ☑ Enable Email Notifications                          │
│ ☑ Enable Browser Notifications                        │
│ ☑ Enable Processing Alerts                            │
│                                                         │
│ Theme: ○ Light  ● Dark  ○ Auto                        │
│                                                         │
│ [Save Preferences]                                     │
└─────────────────────────────────────────────────────────┘
```

### Mobile Interface

#### Responsive Design

The Resume Parser interface is fully responsive and optimized for mobile devices:

**Mobile Features:**
- **Touch-Friendly**: Large buttons and touch targets
- **Swipe Navigation**: Swipe between sections
- **Mobile Upload**: Camera integration for document capture
- **Offline Support**: Basic functionality without internet
- **Progressive Web App**: Install as mobile app

**Mobile Layout:**
```
┌─────────────────┐
│ ☰ Resume Parser │ ← Header with hamburger menu
├─────────────────┤
│                 │
│   📁 Upload     │ ← Large upload button
│                 │
├─────────────────┤
│ Recent Uploads  │ ← Collapsible sections
│ ▼ John Smith    │
│ ▼ Jane Doe      │
├─────────────────┤
│ 🔍 Search       │ ← Search functionality
├─────────────────┤
│ 📊 Stats        │ ← Quick statistics
└─────────────────┘
```

#### Mobile-Specific Features

**Camera Upload:**
1. Tap "Upload" button
2. Select "Take Photo" option
3. Camera interface opens
4. Capture document image
5. Auto-crop and enhance
6. Upload for processing

**Voice Search:**
1. Tap microphone icon in search bar
2. Speak search query
3. Voice-to-text conversion
4. Execute search automatically

**Offline Mode:**
- View previously loaded resumes
- Basic search functionality
- Queue uploads for when online
- Sync when connection restored

## Search Functionality and DTSearch Integration

### Overview

The Resume Parser provides powerful search capabilities through multiple search engines and interfaces. The system combines traditional full-text search with advanced DTSearch functionality, offering users flexible options for finding candidates based on various criteria.

### Search Architecture

#### Search Components

**1. Elasticsearch Integration**
- **Primary Search Engine**: Handles most search operations
- **Full-text Indexing**: Indexes all resume content
- **Real-time Updates**: Automatically indexes new resumes
- **Scalable Performance**: Handles large datasets efficiently

**2. DTSearch Engine**
- **Advanced Boolean Search**: Complex query capabilities
- **Field-specific Search**: Target specific resume fields
- **Proximity Search**: Find terms within specified distances
- **Pattern Matching**: Regular expressions and wildcards

**3. Search Service Layer**
- **Unified Interface**: Single API for all search operations
- **Query Translation**: Converts user queries to engine-specific formats
- **Result Aggregation**: Combines results from multiple sources
- **Caching**: Improves performance for common queries

#### Search Data Flow

```
User Query → Search Interface → Search Service → Search Engines
     ↓              ↓              ↓              ↓
Query Input → Query Processing → Engine Selection → Index Search
     ↓              ↓              ↓              ↓
Results Display ← Result Formatting ← Result Aggregation ← Raw Results
```

### Elasticsearch Search

#### Index Structure

The Elasticsearch index (`cv_documents`) contains structured resume data:

**Document Schema:**
```json
{
  "id": "resume_12345",
  "timestamp": "2024-01-15T10:30:00Z",
  "personal_info": {
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com",
    "phone": "+1-555-123-4567",
    "location": "New York, NY",
    "date_of_birth": "1990-05-15"
  },
  "professional_info": {
    "current_employer": "Tech Corp",
    "years_of_experience": 8,
    "total_experience_months": 96,
    "availability": "Immediate"
  },
  "skills": {
    "technical_skills": ["Python", "JavaScript", "React", "AWS"],
    "expertise_areas": ["Software Development", "Cloud Architecture"],
    "sectors": ["Technology", "Financial Services"],
    "languages_spoken": ["English", "Spanish"]
  },
  "education": {
    "degrees": ["Bachelor of Computer Science"],
    "institutions": ["MIT"],
    "graduation_years": [2012]
  },
  "file_info": {
    "original_filename": "john_smith_resume.pdf",
    "file_type": "PDF",
    "upload_date": "2024-01-15"
  },
  "full_text": "Complete extracted text content..."
}
```

#### Search Query Types

**1. Simple Text Search**
```
# Basic keyword search
Python developer

# Phrase search
"senior software engineer"

# Multiple terms
Python React AWS
```

**2. Field-Specific Search**
```
# Search in specific fields
first_name:John
email:@gmail.com
location:"New York"
skills:Python
```

**3. Range Queries**
```
# Experience range
years_of_experience:[5 TO 10]

# Date range
upload_date:[2024-01-01 TO 2024-12-31]

# Age range
age:[25 TO 35]
```

**4. Boolean Queries**
```
# AND operation
Python AND React

# OR operation
Python OR Java

# NOT operation
Python NOT Java

# Complex combinations
(Python OR Java) AND (React OR Angular) NOT junior
```

#### Search Features

**Fuzzy Search:**
- Handles typos and misspellings
- Configurable edit distance
- Automatic suggestion corrections

**Stemming:**
- Finds word variations
- Example: "develop" matches "developer", "development", "developing"

**Highlighting:**
- Highlights matching terms in results
- Configurable highlight tags
- Context-aware snippets

**Aggregations:**
- Faceted search results
- Count by categories (skills, location, experience)
- Statistical analysis

### DTSearch Integration

#### DTSearch Capabilities

DTSearch provides advanced search features beyond standard full-text search:

**1. Boolean Search Operators**

**Basic Operators:**
- **AND**: Both terms must be present
- **OR**: Either term can be present
- **NOT**: Exclude documents with this term
- **XOR**: Exclusive OR (one term but not both)

**Proximity Operators:**
- **NEAR**: Terms within default distance (usually 10 words)
- **NEAR/n**: Terms within n words of each other
- **BEFORE**: First term must appear before second
- **AFTER**: First term must appear after second

**Example Queries:**
```
# Basic boolean
Python AND React

# Proximity search
Python NEAR/5 developer

# Ordered proximity
senior BEFORE developer

# Complex combinations
(Python OR Java) AND (React OR Angular) NEAR/10 experience
```

**2. Wildcard and Pattern Matching**

**Wildcards:**
- **\***: Matches any number of characters
- **?**: Matches single character
- **[abc]**: Matches any character in brackets
- **[a-z]**: Matches any character in range

**Examples:**
```
# Find variations of "develop"
develop*

# Find 4-letter words starting with "prog"
prog????

# Find email patterns
*@gmail.com

# Find phone number patterns
[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]
```

**3. Field-Specific Search**

DTSearch allows targeting specific fields within documents:

```
# Search in name fields
name:(John OR Jane)

# Search in skills with proximity
skills:(Python NEAR/3 React)

# Search in multiple fields
(name:John) AND (skills:Python) AND (location:"New York")

# Exclude from specific fields
NOT email:@competitor.com
```

**4. Numeric and Date Searches**

**Numeric Ranges:**
```
# Experience range
experience:5..10

# Salary range
salary:80000..120000

# Age calculations
age:>25 AND age:<40
```

**Date Searches:**
```
# Specific date
upload_date:2024-01-15

# Date range
upload_date:2024-01-01..2024-12-31

# Relative dates
upload_date:>-30d  # Last 30 days
graduation_year:>2020
```

#### DTSearch Query Builder

The web interface provides a visual query builder for DTSearch:

**Query Builder Interface:**
```
┌─────────────────────────────────────────────────────────┐
│ DTSearch Query Builder                                  │
├─────────────────────────────────────────────────────────┤
│ Field: [All Fields ▼] Operator: [Contains ▼]          │
│ Value: [Python                                    ]     │
│                                                         │
│ [AND ▼] Field: [Skills ▼] Operator: [Contains ▼]      │
│ Value: [React                                     ]     │
│                                                         │
│ [NOT ▼] Field: [Experience ▼] Operator: [Less Than ▼] │
│ Value: [2                                         ]     │
│                                                         │
│ Generated Query: Python AND skills:React NOT experience:<2 │
│                                                         │
│ [Add Condition] [Remove] [Clear All] [Search]          │
└─────────────────────────────────────────────────────────┘
```

**Available Operators:**
- **Contains**: Field contains the term
- **Exact Match**: Field exactly matches the term
- **Starts With**: Field starts with the term
- **Ends With**: Field ends with the term
- **Greater Than**: Numeric/date comparison
- **Less Than**: Numeric/date comparison
- **Between**: Range comparison
- **Is Empty**: Field has no value
- **Is Not Empty**: Field has a value

### Advanced Search Features

#### Saved Searches

**Creating Saved Searches:**
1. Build your search query
2. Click "Save Search" button
3. Enter search name and description
4. Set sharing permissions
5. Save for future use

**Managing Saved Searches:**
```
┌─────────────────────────────────────────────────────────┐
│ Saved Searches                                          │
├─────────────────────────────────────────────────────────┤
│ ⭐ Senior Python Developers                             │
│    Query: Python AND senior AND experience:>5          │
│    Created: 2024-01-10 | Used: 15 times               │
│    [Run] [Edit] [Share] [Delete]                       │
│ ─────────────────────────────────────────────────────── │
│ 📊 React Frontend Engineers                             │
│    Query: React AND (frontend OR "front-end")          │
│    Created: 2024-01-08 | Used: 8 times                │
│    [Run] [Edit] [Share] [Delete]                       │
└─────────────────────────────────────────────────────────┘
```

#### Search Alerts

**Setting Up Alerts:**
1. Create or run a search query
2. Click "Create Alert" button
3. Configure alert settings:
   - **Frequency**: Real-time, Daily, Weekly
   - **Delivery**: Email, In-app notification
   - **Threshold**: Minimum number of new results
4. Save alert configuration

**Alert Management:**
```
┌─────────────────────────────────────────────────────────┐
│ Search Alerts                                           │
├─────────────────────────────────────────────────────────┤
│ 🔔 Senior Python Developers                             │
│    Frequency: Daily | Last triggered: 2 hours ago      │
│    New results: 3 candidates                           │
│    [View Results] [Edit] [Pause] [Delete]              │
│ ─────────────────────────────────────────────────────── │
│ 📧 Machine Learning Engineers                           │
│    Frequency: Weekly | Last triggered: 2 days ago      │
│    New results: 0 candidates                           │
│    [View Results] [Edit] [Pause] [Delete]              │
└─────────────────────────────────────────────────────────┘
```

#### Search Analytics

**Search Performance Metrics:**

**Query Performance:**
```
┌─────────────────────────────────────────────────────────┐
│ Search Performance (Last 30 Days)                      │
├─────────────────────────────────────────────────────────┤
│ Total Searches: 2,847                                  │
│ Average Response Time: 0.23 seconds                    │
│ Cache Hit Rate: 67%                                    │
│ Failed Queries: 12 (0.4%)                             │
└─────────────────────────────────────────────────────────┘
```

**Popular Search Terms:**
1. Python (1,247 searches)
2. React (892 searches)
3. Senior (756 searches)
4. JavaScript (634 searches)
5. AWS (523 searches)

**Search Patterns:**
- **Peak Hours**: 9-11 AM, 2-4 PM
- **Most Active Days**: Tuesday, Wednesday
- **Average Results per Query**: 23.4
- **Zero-Result Queries**: 8.2%

### Search Optimization

#### Index Optimization

**Elasticsearch Index Settings:**
```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "resume_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "stop",
            "stemmer",
            "synonym"
          ]
        }
      },
      "filter": {
        "synonym": {
          "type": "synonym",
          "synonyms": [
            "js,javascript",
            "react,reactjs",
            "python,py",
            "ai,artificial intelligence"
          ]
        }
      }
    }
  }
}
```

**Performance Tuning:**
- **Bulk Indexing**: Process multiple documents simultaneously
- **Refresh Intervals**: Optimize for search vs. indexing performance
- **Memory Management**: Configure heap size and caching
- **Shard Distribution**: Balance load across cluster nodes

#### Query Optimization

**Best Practices:**

**1. Use Specific Fields**
```
# Better: Target specific fields
skills:Python AND location:"New York"

# Avoid: Generic full-text search
Python New York
```

**2. Limit Result Size**
```
# Use pagination
from=0&size=25

# Avoid large result sets
size=1000  # Can cause performance issues
```

**3. Use Filters for Exact Matches**
```
# Better: Use filters for exact values
filter: {"term": {"file_type": "PDF"}}

# Avoid: Text search for exact values
query: "file_type:PDF"
```

**4. Cache Common Queries**
- Enable query result caching
- Use consistent query formats
- Implement application-level caching

### Search API Reference

#### REST API Endpoints

**Basic Search:**
```http
POST /api/search/
Content-Type: application/json

{
  "query": "Python developer",
  "filters": {
    "experience_min": 3,
    "location": "New York"
  },
  "page": 1,
  "page_size": 25,
  "sort": "relevance"
}
```

**Advanced Search:**
```http
POST /api/search/advanced/
Content-Type: application/json

{
  "elasticsearch_query": {
    "bool": {
      "must": [
        {"match": {"skills": "Python"}},
        {"range": {"years_of_experience": {"gte": 3}}}
      ]
    }
  },
  "highlight": {
    "fields": {
      "skills": {},
      "full_text": {}
    }
  }
}
```

**DTSearch Query:**
```http
POST /api/search/dtsearch/
Content-Type: application/json

{
  "query": "Python AND React NEAR/5 experience",
  "options": {
    "case_sensitive": false,
    "whole_words_only": false,
    "fuzzy_search": true,
    "stemming": true
  },
  "fields": ["skills", "full_text", "job_titles"],
  "max_results": 100
}
```

#### Response Format

**Search Response:**
```json
{
  "status": "success",
  "query": "Python developer",
  "total_results": 247,
  "page": 1,
  "page_size": 25,
  "total_pages": 10,
  "search_time_ms": 23,
  "results": [
    {
      "id": "resume_12345",
      "score": 0.95,
      "candidate": {
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-123-4567",
        "location": "New York, NY",
        "experience_years": 8
      },
      "highlights": {
        "skills": ["<em>Python</em>", "React", "AWS"],
        "full_text": ["Senior <em>Python developer</em> with 8 years..."]
      },
      "metadata": {
        "upload_date": "2024-01-15T10:30:00Z",
        "file_type": "PDF",
        "processing_status": "completed"
      }
    }
  ],
  "aggregations": {
    "experience_levels": {
      "entry": 23,
      "mid": 156,
      "senior": 68
    },
    "locations": {
      "New York, NY": 89,
      "San Francisco, CA": 67,
      "Seattle, WA": 45
    },
    "skills": {
      "Python": 247,
      "React": 156,
      "JavaScript": 134
    }
  }
}
```

### Search Troubleshooting

#### Common Issues

**1. No Search Results**

**Possible Causes:**
- Typos in search terms
- Too restrictive filters
- Index not updated
- Search terms not in indexed content

**Solutions:**
```
# Check for typos
Original: "Pythom developer"
Corrected: "Python developer"

# Broaden search terms
Original: "Senior Python React AWS 10+ years"
Simplified: "Python React"

# Check index status
GET /api/search/status/

# Verify document indexing
GET /api/resumes/{id}/search-data/
```

**2. Slow Search Performance**

**Diagnostics:**
```
# Check search performance
GET /api/search/performance/

# Monitor Elasticsearch cluster
GET /_cluster/health
GET /_nodes/stats

# Analyze slow queries
GET /_search/slow_log
```

**Optimization Steps:**
1. **Reduce Result Size**: Limit page size to 25-50 results
2. **Use Filters**: Replace queries with filters where possible
3. **Optimize Queries**: Avoid wildcard queries at the beginning of terms
4. **Index Tuning**: Adjust refresh intervals and memory settings

**3. Inconsistent Results**

**Possible Causes:**
- Index synchronization issues
- Caching problems
- Concurrent updates

**Solutions:**
```
# Force index refresh
POST /api/search/refresh/

# Clear search cache
DELETE /api/search/cache/

# Reindex specific document
POST /api/resumes/{id}/reindex/

# Full reindex (use with caution)
POST /api/search/reindex-all/
```

#### Performance Monitoring

**Key Metrics to Monitor:**

**Search Performance:**
- Average query response time
- 95th percentile response time
- Queries per second
- Cache hit ratio
- Failed query percentage

**Index Health:**
- Index size and growth rate
- Document count
- Indexing rate
- Memory usage
- Disk space utilization

**Monitoring Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│ Search Performance Dashboard                            │
├─────────────────────────────────────────────────────────┤
│ Response Time: 0.23s avg | 0.45s p95                  │
│ Throughput: 45 queries/sec                             │
│ Cache Hit Rate: 67%                                    │
│ Error Rate: 0.2%                                       │
│                                                         │
│ Index Status: ● Healthy                                │
│ Documents: 125,847                                     │
│ Index Size: 2.3 GB                                    │
│ Memory Usage: 1.2 GB / 4.0 GB                         │
└─────────────────────────────────────────────────────────┘
```

## Deployment and Production Setup

### Overview

This section provides comprehensive guidance for deploying the Resume Parser application to production environments. The system supports multiple deployment strategies including cloud platforms, containerized deployments, and traditional server setups.

### Deployment Architecture

#### Production Components

```
┌─────────────────────────────────────────────────────────┐
│                Production Architecture                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Frontend  │    │   Backend   │    │  Database   │ │
│  │  (Vercel)   │◄──►│  (Render)   │◄──►│(PostgreSQL) │ │
│  │             │    │             │    │             │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                   │                   │       │
│         │                   │                   │       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │     CDN     │    │ File Storage│    │ Search Index│ │
│  │  (Vercel)   │    │   (S3/GCS)  │    │(Elasticsearch)│ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ QueryMind   │    │ Monitoring  │    │   Backup    │ │
│  │ Integration │    │ (DataDog)   │    │  (Automated)│ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Cloud Platform Deployment

#### Vercel Frontend Deployment

**Prerequisites:**
- Vercel account
- GitHub repository
- Node.js 18+ locally

**Step 1: Prepare Frontend**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Test production build locally
npm start
```

**Step 2: Configure Environment Variables**

Create `.env.production` file:
```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_ENVIRONMENT=production

# Analytics (Optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_HOTJAR_ID=XXXXXXX

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_SEARCH=true
NEXT_PUBLIC_ENABLE_QUERYMIND=true

# Upload Configuration
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
NEXT_PUBLIC_ALLOWED_FILE_TYPES=pdf,doc,docx,rtf,txt
```

**Step 3: Deploy to Vercel**

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

**Option B: GitHub Integration**
1. Connect GitHub repository to Vercel
2. Configure build settings:
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
3. Add environment variables in Vercel dashboard
4. Deploy automatically on push to main branch

**Step 4: Configure Custom Domain (Optional)**
```bash
# Add custom domain
vercel domains add yourdomain.com

# Configure DNS
# Add CNAME record: www -> cname.vercel-dns.com
# Add A record: @ -> 76.76.19.61
```

#### Render Backend Deployment

**Prerequisites:**
- Render account
- GitHub repository
- PostgreSQL database

**Step 1: Prepare Backend**
```bash
# Navigate to backend directory
cd backend

# Create requirements.txt if not exists
pip freeze > requirements.txt

# Create runtime.txt for Python version
echo "python-3.11.0" > runtime.txt
```

**Step 2: Configure Build Settings**

Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: resume-parser-backend
    env: python
    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
    startCommand: |
      gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: resume-parser-db
          property: connectionString
      - key: ALLOWED_HOSTS
        value: your-app.onrender.com,yourdomain.com
      - key: CORS_ALLOWED_ORIGINS
        value: https://your-frontend.vercel.app,https://yourdomain.com
      - key: OPENAI_API_KEY
        sync: false
      - key: GOOGLE_API_KEY
        sync: false
      - key: ELASTICSEARCH_URL
        value: https://your-elasticsearch-cluster.com
      - key: AWS_ACCESS_KEY_ID
        sync: false
      - key: AWS_SECRET_ACCESS_KEY
        sync: false
      - key: AWS_STORAGE_BUCKET_NAME
        value: your-resume-bucket
      - key: AWS_S3_REGION_NAME
        value: us-east-1

databases:
  - name: resume-parser-db
    databaseName: resume_parser
    user: resume_user
```

**Step 3: Deploy to Render**

1. **Create New Web Service**:
   - Connect GitHub repository
   - Select backend directory
   - Configure build and start commands

2. **Database Setup**:
   ```sql
   -- Create database
   CREATE DATABASE resume_parser;
   CREATE USER resume_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_user;
   ```

3. **Environment Variables**:
   ```env
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   
   # AI Provider Keys
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=AIza...
   
   # File Storage
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   AWS_STORAGE_BUCKET_NAME=resume-files
   AWS_S3_REGION_NAME=us-east-1
   
   # Search
   ELASTICSEARCH_URL=https://elastic:password@host:port
   
   # File Upload Settings
   MAX_UPLOAD_SIZE=10485760
   ALLOWED_FILE_TYPES=pdf,doc,docx,rtf,txt
   
   # Frontend URL
   FRONTEND_URL=https://your-frontend.vercel.app
   ```

4. **Deploy and Monitor**:
   ```bash
   # Monitor deployment logs
   render logs --service resume-parser-backend --tail
   
   # Check service status
   render services list
   ```

### Docker Deployment

#### Docker Compose Setup

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: resume_parser
      POSTGRES_USER: resume_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U resume_user -d resume_parser"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes

  # Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://resume_user:${DB_PASSWORD}@db:5432/resume_parser
      - REDIS_URL=redis://redis:6379/0
      - ELASTICSEARCH_URL=http://elasticsearch:9200
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      elasticsearch:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/api/health/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_ENVIRONMENT=production
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

  # QueryMind Integration
  querymind:
    build:
      context: ./QueryMind
      dockerfile: Dockerfile
    environment:
      - RESUME_PARSER_URL=http://backend:8000
      - SOURCE_FOLDER=/watched_folder
      - INTEGRATION_ENABLED=true
      - LOG_LEVEL=INFO
    volumes:
      - ./watched_folder:/watched_folder
      - ./logs/querymind:/app/logs
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:

networks:
  default:
    driver: bridge
```

**Backend Dockerfile.prod:**
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings.production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs /app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "backend.wsgi:application"]
```

**Frontend Dockerfile.prod:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
```

**Nginx Configuration:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=upload:10m rate=2r/s;
    
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;
        
        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Increase timeouts for file uploads
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
        
        # File upload endpoint
        location /api/upload/ {
            limit_req zone=upload burst=5 nodelay;
            client_max_body_size 10M;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Extended timeouts for large files
            proxy_connect_timeout 300s;
            proxy_send_timeout 300s;
            proxy_read_timeout 300s;
        }
        
        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Media files
        location /media/ {
            alias /app/media/;
            expires 1y;
            add_header Cache-Control "public";
        }
        
        # Frontend routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

**Deployment Commands:**
```bash
# Create environment file
cp .env.example .env.prod

# Edit environment variables
vim .env.prod

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Kubernetes Deployment

#### Kubernetes Manifests

**namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: resume-parser
```

**configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: resume-parser-config
  namespace: resume-parser
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "resume-parser.yourdomain.com"
  CORS_ALLOWED_ORIGINS: "https://resume-parser.yourdomain.com"
  MAX_UPLOAD_SIZE: "10485760"
  ALLOWED_FILE_TYPES: "pdf,doc,docx,rtf,txt"
  ELASTICSEARCH_URL: "http://elasticsearch:9200"
  REDIS_URL: "redis://redis:6379/0"
```

**secrets.yaml:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: resume-parser-secrets
  namespace: resume-parser
type: Opaque
data:
  SECRET_KEY: <base64-encoded-secret>
  DATABASE_URL: <base64-encoded-db-url>
  OPENAI_API_KEY: <base64-encoded-openai-key>
  GOOGLE_API_KEY: <base64-encoded-google-key>
  AWS_ACCESS_KEY_ID: <base64-encoded-aws-key>
  AWS_SECRET_ACCESS_KEY: <base64-encoded-aws-secret>
```

**backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: resume-parser
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/resume-parser-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: resume-parser-config
        - secretRef:
            name: resume-parser-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**backend-service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: resume-parser
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: resume-parser-ingress
  namespace: resume-parser
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
  - hosts:
    - resume-parser.yourdomain.com
    secretName: resume-parser-tls
  rules:
  - host: resume-parser.yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 3000
```

**Deploy to Kubernetes:**
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n resume-parser

# View logs
kubectl logs -f deployment/backend -n resume-parser

# Scale deployment
kubectl scale deployment backend --replicas=5 -n resume-parser
```

### Database Setup and Migration

#### PostgreSQL Production Setup

**Database Configuration:**
```sql
-- Create database and user
CREATE DATABASE resume_parser;
CREATE USER resume_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_user;

-- Configure for production
ALTER DATABASE resume_parser SET timezone TO 'UTC';
ALTER USER resume_user SET default_transaction_isolation TO 'read committed';
ALTER USER resume_user SET timezone TO 'UTC';

-- Performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
SELECT pg_reload_conf();
```

**Migration Commands:**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (if any)
python manage.py loaddata initial_data.json

# Create search index
python manage.py create_search_index
```

#### Database Backup Strategy

**Automated Backup Script:**
```bash
#!/bin/bash
# backup_db.sh

DB_NAME="resume_parser"
DB_USER="resume_user"
DB_HOST="localhost"
BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/resume_parser_${DATE}.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Upload to S3 (optional)
aws s3 cp ${BACKUP_FILE}.gz s3://your-backup-bucket/database/

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "resume_parser_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

**Cron Job Setup:**
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup_db.sh

# Weekly full backup at 3 AM on Sundays
0 3 * * 0 /path/to/full_backup.sh
```

### Monitoring and Logging

#### Application Monitoring

**Health Check Endpoints:**
```python
# backend/apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
import elasticsearch

def health_check(request):
    """Comprehensive health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'services': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['services']['database'] = 'healthy'
    except Exception as e:
        status['services']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Redis check
    try:
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        status['services']['redis'] = 'healthy'
    except Exception as e:
        status['services']['redis'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Elasticsearch check
    try:
        from apps.search.services import SearchService
        search_service = SearchService()
        search_service.client.cluster.health()
        status['services']['elasticsearch'] = 'healthy'
    except Exception as e:
        status['services']['elasticsearch'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    return JsonResponse(status)
```

**Prometheus Metrics:**
```python
# backend/apps/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Application metrics
resume_uploads = Counter(
    'resume_uploads_total',
    'Total resume uploads',
    ['status']
)

processing_duration = Histogram(
    'resume_processing_duration_seconds',
    'Resume processing duration'
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

search_queries = Counter(
    'search_queries_total',
    'Total search queries',
    ['engine']
)
```

#### Logging Configuration

**Django Logging Settings:**
```python
# backend/settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django_errors.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.ai_parser': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.search': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Security Configuration

#### SSL/TLS Setup

**Let's Encrypt with Certbot:**
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

**Security Headers:**
```python
# backend/settings/production.py

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
```

#### Environment Security

**Secrets Management:**
```bash
# Use environment variables for secrets
export SECRET_KEY="$(openssl rand -base64 32)"
export DATABASE_PASSWORD="$(openssl rand -base64 32)"

# Or use a secrets management service
# AWS Secrets Manager
aws secretsmanager create-secret \
    --name resume-parser/prod/database \
    --secret-string '{"password":"your-secure-password"}'

# HashiCorp Vault
vault kv put secret/resume-parser/prod \
    database_password="your-secure-password" \
    secret_key="your-secret-key"
```

### Performance Optimization

#### Database Optimization

**Index Creation:**
```sql
-- Performance indexes
CREATE INDEX CONCURRENTLY idx_resumes_timestamp ON resumes_resume(timestamp);
CREATE INDEX CONCURRENTLY idx_resumes_email ON resumes_resume(email);
CREATE INDEX CONCURRENTLY idx_resumes_skills ON resumes_resume USING GIN(skill_keywords);
CREATE INDEX CONCURRENTLY idx_resumes_location ON resumes_resume(location);
CREATE INDEX CONCURRENTLY idx_resumes_experience ON resumes_resume(years_of_experience);

-- Partial indexes for common queries
CREATE INDEX CONCURRENTLY idx_resumes_active 
    ON resumes_resume(timestamp) 
    WHERE processing_status = 'completed';
```

**Query Optimization:**
```python
# Use select_related and prefetch_related
resumes = Resume.objects.select_related('user').prefetch_related('skills')

# Use database functions
from django.db.models import Count, Avg
stats = Resume.objects.aggregate(
    total_count=Count('id'),
    avg_experience=Avg('years_of_experience')
)

# Use raw SQL for complex queries
resumes = Resume.objects.raw(
    "SELECT * FROM resumes_resume WHERE skills @> %s",
    [json.dumps(['Python'])]
)
```

#### Caching Strategy

**Redis Configuration:**
```python
# backend/settings/production.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'resume_parser',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Cache configuration
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'resume_parser'
```

**Application Caching:**
```python
# Cache search results
from django.core.cache import cache

def search_resumes(query, filters):
    cache_key = f"search:{hash(query)}:{hash(str(filters))}"
    results = cache.get(cache_key)
    
    if results is None:
        results = perform_search(query, filters)
        cache.set(cache_key, results, timeout=300)
    
    return results

# Cache expensive computations
@cache_result(timeout=3600)
def get_resume_statistics():
    return {
        'total_resumes': Resume.objects.count(),
        'processed_today': Resume.objects.filter(
            timestamp__date=timezone.now().date()
        ).count(),
        'top_skills': get_top_skills(),
    }
```

### Backup and Disaster Recovery

#### Backup Strategy

**Automated Backup System:**
```bash
#!/bin/bash
# comprehensive_backup.sh

BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/backups/${BACKUP_DATE}"
S3_BUCKET="your-backup-bucket"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "Backing up database..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/database.sql

# File uploads backup
echo "Backing up uploaded files..."
tar -czf $BACKUP_DIR/uploads.tar.gz /app/uploads/

# Configuration backup
echo "Backing up configuration..."
cp -r /app/config/ $BACKUP_DIR/

# Elasticsearch backup
echo "Backing up search index..."
curl -X PUT "elasticsearch:9200/_snapshot/backup_repo/$BACKUP_DATE" -H 'Content-Type: application/json' -d'{
  "indices": "cv_documents",
  "ignore_unavailable": true,
  "include_global_state": false
}'

# Compress entire backup
tar -czf /backups/backup_${BACKUP_DATE}.tar.gz -C /backups $BACKUP_DATE

# Upload to S3
aws s3 cp /backups/backup_${BACKUP_DATE}.tar.gz s3://$S3_BUCKET/backups/

# Clean local backups (keep last 7 days)
find /backups -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: backup_${BACKUP_DATE}.tar.gz"
```

#### Disaster Recovery Plan

**Recovery Procedures:**

**1. Database Recovery:**
```bash
# Stop application
docker-compose down

# Restore database
psql -h $DB_HOST -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS resume_parser;"
psql -h $DB_HOST -U $DB_USER -d postgres -c "CREATE DATABASE resume_parser;"
psql -h $DB_HOST -U $DB_USER -d resume_parser < backup/database.sql

# Restart application
docker-compose up -d
```

**2. File Recovery:**
```bash
# Extract uploaded files
tar -xzf backup/uploads.tar.gz -C /

# Set correct permissions
chown -R appuser:appuser /app/uploads/
```

**3. Search Index Recovery:**
```bash
# Restore Elasticsearch snapshot
curl -X POST "elasticsearch:9200/_snapshot/backup_repo/backup_20240115/_restore" -H 'Content-Type: application/json' -d'{
  "indices": "cv_documents",
  "ignore_unavailable": true,
  "include_global_state": false
}'

# Or rebuild from database
python manage.py rebuild_search_index
```

**Recovery Testing:**
```bash
# Monthly recovery test
#!/bin/bash
# test_recovery.sh

echo "Starting recovery test..."

# Create test environment
docker-compose -f docker-compose.test.yml up -d

# Restore latest backup
latest_backup=$(aws s3 ls s3://$S3_BUCKET/backups/ | sort | tail -n 1 | awk '{print $4}')
aws s3 cp s3://$S3_BUCKET/backups/$latest_backup /tmp/

# Extract and restore
tar -xzf /tmp/$latest_backup -C /tmp/
./restore_backup.sh /tmp/backup_*/

# Run health checks
curl -f http://localhost:8000/api/health/ || exit 1

# Cleanup test environment
docker-compose -f docker-compose.test.yml down

echo "Recovery test completed successfully"
```

## Troubleshooting and Maintenance

### Common Issues and Solutions

#### Application Startup Issues

**Problem: Backend fails to start**

*Symptoms:*
- Django server won't start
- Database connection errors
- Import errors

*Solutions:*
```bash
# Check Python environment
python --version  # Should be 3.8+
pip list | grep Django  # Verify Django installation

# Check database connection
python manage.py dbshell
# If fails, verify DATABASE_URL in settings

# Check for missing dependencies
pip install -r requirements.txt

# Check for migration issues
python manage.py showmigrations
python manage.py migrate

# Check for port conflicts
netstat -tulpn | grep :8000
# Kill conflicting process if needed
sudo kill -9 <PID>
```

**Problem: Frontend fails to start**

*Symptoms:*
- Next.js build errors
- Module not found errors
- Port conflicts

*Solutions:*
```bash
# Check Node.js version
node --version  # Should be 18+
npm --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Check for TypeScript errors
npm run type-check

# Check environment variables
cat .env.local
# Ensure NEXT_PUBLIC_API_URL is set correctly

# Check for port conflicts
lsof -i :3000
# Use different port if needed
npm run dev -- -p 3001
```

#### File Upload Issues

**Problem: File uploads fail**

*Symptoms:*
- "File too large" errors
- Upload timeouts
- Unsupported file type errors

*Solutions:*
```python
# Check Django settings
# backend/settings.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Check allowed file types
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'rtf', 'txt']

# Check file permissions
ls -la uploads/
sudo chown -R www-data:www-data uploads/
sudo chmod -R 755 uploads/
```

```nginx
# Check Nginx configuration
# /etc/nginx/sites-available/resume-parser
client_max_body_size 10M;
proxy_read_timeout 300;
proxy_connect_timeout 300;
proxy_send_timeout 300;
```

**Problem: File processing fails**

*Symptoms:*
- Files uploaded but not processed
- AI parsing errors
- Text extraction failures

*Solutions:*
```bash
# Check AI provider API keys
echo $OPENAI_API_KEY
echo $GOOGLE_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models

# Check file format support
python -c "import unstructured; print('Unstructured installed')"
python -c "import docx; print('python-docx installed')"
python -c "import PyPDF2; print('PyPDF2 installed')"

# Check processing logs
tail -f logs/django.log | grep "ai_parser"

# Manually test file processing
python manage.py shell
>>> from apps.ai_parser.services import ResumeParsingService
>>> service = ResumeParsingService()
>>> result = service.parse_resume('/path/to/test.pdf')
```

#### Search Issues

**Problem: Search not working**

*Symptoms:*
- No search results
- Elasticsearch connection errors
- Search index missing

*Solutions:*
```bash
# Check Elasticsearch status
curl -X GET "localhost:9200/_cluster/health?pretty"

# Check if index exists
curl -X GET "localhost:9200/_cat/indices?v"

# Recreate search index
python manage.py shell
>>> from apps.search.services import SearchService
>>> service = SearchService()
>>> service.create_index()

# Reindex all documents
python manage.py rebuild_search_index

# Check index mapping
curl -X GET "localhost:9200/cv_documents/_mapping?pretty"

# Test search manually
curl -X POST "localhost:9200/cv_documents/_search" \
     -H 'Content-Type: application/json' \
     -d '{
       "query": {
         "match": {
           "content": "python"
         }
       }
     }'
```

**Problem: DTSearch integration issues**

*Symptoms:*
- DTSearch queries fail
- Syntax errors in search
- Performance issues

*Solutions:*
```python
# Check DTSearch configuration
# apps/search/services.py
class SearchService:
    def __init__(self):
        # Verify DTSearch settings
        self.dtsearch_enabled = getattr(settings, 'DTSEARCH_ENABLED', False)
        self.dtsearch_index_path = getattr(settings, 'DTSEARCH_INDEX_PATH', '')

# Test DTSearch syntax
from apps.search.services import SearchService
service = SearchService()

# Valid DTSearch queries
results = service.search_documents("python AND django")
results = service.search_documents("experience NEAR/5 years")
results = service.search_documents("skill* AND (java OR python)")

# Check for syntax errors
try:
    results = service.search_documents("invalid AND (query")
except Exception as e:
    print(f"Syntax error: {e}")
```

#### QueryMind Integration Issues

**Problem: QueryMind not detecting files**

*Symptoms:*
- Files added to watched folder but not processed
- No file detection logs
- Integration appears inactive

*Solutions:*
```bash
# Check QueryMind status
cd QueryMind
python integration_manager.py --status

# Check configuration
cat main.py | grep -E "SOURCE_FOLDER|RESUME_PARSER_URL|INTEGRATION_ENABLED"

# Verify folder permissions
ls -la /path/to/watched/folder
sudo chmod -R 755 /path/to/watched/folder

# Check file watcher logs
tail -f logs/querymind.log

# Test file detection manually
cp test_resume.pdf /path/to/watched/folder/
# Should see detection in logs within 5 seconds

# Restart QueryMind
python integration_manager.py --disable
python integration_manager.py --enable
python main.py
```

**Problem: Backend connection issues**

*Symptoms:*
- QueryMind can't reach backend API
- HTTP connection errors
- Authentication failures

*Solutions:*
```bash
# Test backend connectivity
curl -X GET "http://localhost:8000/api/health/"

# Check network configuration
ping localhost
telnet localhost 8000

# Verify API endpoints
curl -X POST "http://localhost:8000/api/resumes/upload/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_resume.pdf"

# Check firewall settings
sudo ufw status
sudo iptables -L

# Update QueryMind configuration
# main.py
RESUME_PARSER_URL = "http://127.0.0.1:8000"  # Try different localhost format
RESUME_PARSER_URL = "http://backend:8000"     # For Docker environments
```

#### Performance Issues

**Problem: Slow response times**

*Symptoms:*
- API requests taking too long
- File processing delays
- Search queries slow

*Solutions:*
```python
# Enable Django debug toolbar (development only)
# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Check database query performance
from django.db import connection
from django.conf import settings

settings.LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}

# Optimize database queries
from apps.resumes.models import Resume

# Bad: N+1 queries
resumes = Resume.objects.all()
for resume in resumes:
    print(resume.user.email)  # Triggers additional query

# Good: Use select_related
resumes = Resume.objects.select_related('user').all()
for resume in resumes:
    print(resume.user.email)  # No additional query

# Add database indexes
# migrations/xxxx_add_indexes.py
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_resumes_email ON resumes_resume(email);"
        ),
    ]
```

```bash
# Check system resources
top
htop
free -h
df -h

# Monitor database performance
sudo -u postgres psql
\x
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

# Check Elasticsearch performance
curl -X GET "localhost:9200/_nodes/stats/indices?pretty"
curl -X GET "localhost:9200/_cluster/stats?pretty"

# Optimize Elasticsearch
# Increase heap size
export ES_JAVA_OPTS="-Xms2g -Xmx2g"

# Add more replicas for read performance
curl -X PUT "localhost:9200/cv_documents/_settings" \
     -H 'Content-Type: application/json' \
     -d '{
       "index": {
         "number_of_replicas": 2
       }
     }'
```

#### Memory and Resource Issues

**Problem: High memory usage**

*Symptoms:*
- Out of memory errors
- System slowdown
- Process crashes

*Solutions:*
```bash
# Monitor memory usage
free -h
ps aux --sort=-%mem | head

# Check for memory leaks
valgrind --tool=memcheck python manage.py runserver

# Optimize Django settings
# settings.py
DATABASE_CONN_MAX_AGE = 60  # Reuse database connections
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 20,  # Limit Redis connections
            }
        }
    }
}

# Limit file upload size
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# Use streaming for large files
from django.http import StreamingHttpResponse

def download_resume(request, resume_id):
    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    response = StreamingHttpResponse(
        file_iterator(resume.file.path),
        content_type='application/pdf'
    )
    return response
```

### Maintenance Tasks

#### Regular Maintenance Schedule

**Daily Tasks:**
```bash
#!/bin/bash
# daily_maintenance.sh

# Check system health
curl -f http://localhost:8000/api/health/ || echo "Backend health check failed"
curl -f http://localhost:3000/api/health || echo "Frontend health check failed"

# Check disk space
df -h | awk '$5 > 80 {print "Warning: " $0}'

# Check log file sizes
find /var/log -name "*.log" -size +100M -exec ls -lh {} \;

# Rotate logs if needed
logrotate -f /etc/logrotate.d/resume-parser

# Check for failed processes
systemctl status resume-parser-backend
systemctl status resume-parser-frontend
systemctl status querymind

# Clean temporary files
find /tmp -name "resume_*" -mtime +1 -delete
find uploads/temp -name "*" -mtime +1 -delete

# Database maintenance
psql -d resume_parser -c "VACUUM ANALYZE;"

# Check Elasticsearch cluster health
curl -s "localhost:9200/_cluster/health" | jq '.status'
```

**Weekly Tasks:**
```bash
#!/bin/bash
# weekly_maintenance.sh

# Full database backup
./backup_db.sh

# Update search index statistics
python manage.py update_search_stats

# Clean old uploaded files (optional)
find uploads/ -name "*.pdf" -mtime +30 -delete
find uploads/ -name "*.doc*" -mtime +30 -delete

# Optimize database
psql -d resume_parser -c "REINDEX DATABASE resume_parser;"
psql -d resume_parser -c "VACUUM FULL;"

# Update system packages (with caution)
sudo apt update
sudo apt list --upgradable

# Check SSL certificate expiry
openssl x509 -in /etc/ssl/certs/resume-parser.crt -noout -dates

# Generate weekly report
python manage.py generate_weekly_report
```

**Monthly Tasks:**
```bash
#!/bin/bash
# monthly_maintenance.sh

# Security updates
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip list --outdated
pip install -U pip setuptools wheel

# Update Node.js packages
npm audit
npm update

# Clean Docker images (if using Docker)
docker system prune -f
docker image prune -f

# Archive old logs
tar -czf logs/archive/$(date +%Y%m).tar.gz logs/*.log
find logs/ -name "*.log" -mtime +30 -delete

# Performance analysis
python manage.py analyze_performance

# Security scan
nmap -sS localhost
python manage.py check --deploy

# Test disaster recovery
./test_recovery.sh
```

#### Log Management

**Log Rotation Configuration:**
```bash
# /etc/logrotate.d/resume-parser
/app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
    postrotate
        systemctl reload resume-parser-backend
    endscript
}

/var/log/nginx/resume-parser*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload nginx
    endscript
}
```

**Log Analysis Scripts:**
```bash
#!/bin/bash
# analyze_logs.sh

# Error analysis
echo "=== Recent Errors ==="
grep -i error logs/django.log | tail -20

# Performance analysis
echo "=== Slow Requests ==="
grep "slow" logs/django.log | tail -10

# Upload statistics
echo "=== Upload Statistics ==="
grep "upload" logs/django.log | \
    awk '{print $1}' | \
    sort | uniq -c | \
    sort -nr

# Search query analysis
echo "=== Popular Search Terms ==="
grep "search_query" logs/django.log | \
    sed 's/.*search_query: \([^"]*\).*/\1/' | \
    sort | uniq -c | \
    sort -nr | head -10

# AI processing statistics
echo "=== AI Processing Stats ==="
grep "ai_processing" logs/django.log | \
    awk '{print $3}' | \
    awk '{sum+=$1; count++} END {print "Average: " sum/count "s"}'
```

#### Database Maintenance

**Performance Monitoring:**
```sql
-- Check database size
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE mean_time > 100  -- queries taking more than 100ms
ORDER BY mean_time DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Unused indexes

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables;
```

**Database Optimization:**
```sql
-- Update table statistics
ANALYZE;

-- Vacuum tables
VACUUM VERBOSE ANALYZE resumes_resume;
VACUUM VERBOSE ANALYZE auth_user;

-- Reindex if needed
REINDEX INDEX idx_resumes_timestamp;
REINDEX TABLE resumes_resume;

-- Check for bloat
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename)) as size,
    pg_size_pretty(pg_relation_size(tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(tablename) - pg_relation_size(tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'public';
```

#### Security Maintenance

**Security Checklist:**
```bash
#!/bin/bash
# security_check.sh

# Check for security updates
sudo apt list --upgradable | grep -i security

# Verify SSL certificate
openssl s509 -in /etc/ssl/certs/resume-parser.crt -text -noout

# Check file permissions
find /app -type f -perm /o+w -exec ls -l {} \;
find /app -type d -perm /o+w -exec ls -ld {} \;

# Check for suspicious processes
ps aux | grep -E "(nc|netcat|telnet|ssh)"

# Check network connections
netstat -tulpn | grep LISTEN

# Check failed login attempts
grep "Failed password" /var/log/auth.log | tail -10

# Check Django security
python manage.py check --deploy

# Scan for vulnerabilities
nmap -sS -O localhost

# Check for malware (if clamav installed)
clamscan -r /app/uploads/
```

**Security Updates:**
```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Update Python packages
pip list --outdated
pip install --upgrade pip
pip-review --auto  # If pip-review is installed

# Update Node.js packages
npm audit
npm audit fix
npm update

# Check for Django security releases
pip install --upgrade Django

# Update Docker images
docker pull python:3.11-slim
docker pull node:18-alpine
docker pull postgres:15
docker pull redis:7-alpine
docker pull nginx:alpine
```

### Monitoring and Alerting

#### Health Check Monitoring

**Monitoring Script:**
```bash
#!/bin/bash
# monitor_health.sh

SERVICES=(
    "http://localhost:8000/api/health/"
    "http://localhost:3000/api/health"
    "http://localhost:9200/_cluster/health"
)

for service in "${SERVICES[@]}"; do
    if curl -f -s "$service" > /dev/null; then
        echo "✓ $service is healthy"
    else
        echo "✗ $service is unhealthy"
        # Send alert (email, Slack, etc.)
        ./send_alert.sh "Service $service is down"
    fi
done

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "⚠ Disk usage is ${DISK_USAGE}%"
    ./send_alert.sh "High disk usage: ${DISK_USAGE}%"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt 80 ]; then
    echo "⚠ Memory usage is ${MEM_USAGE}%"
    ./send_alert.sh "High memory usage: ${MEM_USAGE}%"
fi
```

**Alert Script:**
```bash
#!/bin/bash
# send_alert.sh

MESSAGE="$1"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Email alert
echo "[$TIMESTAMP] $MESSAGE" | \
    mail -s "Resume Parser Alert" admin@yourdomain.com

# Slack alert (if webhook configured)
if [ -n "$SLACK_WEBHOOK" ]; then
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"[$TIMESTAMP] $MESSAGE\"}" \
        "$SLACK_WEBHOOK"
fi

# Log alert
echo "[$TIMESTAMP] ALERT: $MESSAGE" >> /var/log/resume-parser-alerts.log
```

#### Performance Monitoring

**Performance Metrics Collection:**
```python
# apps/core/monitoring.py
import time
import psutil
from django.core.cache import cache
from django.db import connection
from prometheus_client import Counter, Histogram, Gauge

# Metrics
request_count = Counter('http_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'Request duration')
system_memory = Gauge('system_memory_usage_percent', 'Memory usage percentage')
system_cpu = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
database_connections = Gauge('database_connections_active', 'Active database connections')

class MonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Record metrics
        duration = time.time() - start_time
        request_count.labels(
            method=request.method,
            endpoint=request.path
        ).inc()
        request_duration.observe(duration)
        
        return response

def collect_system_metrics():
    """Collect system metrics"""
    # Memory usage
    memory = psutil.virtual_memory()
    system_memory.set(memory.percent)
    
    # CPU usage
    cpu = psutil.cpu_percent(interval=1)
    system_cpu.set(cpu)
    
    # Database connections
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
        )
        active_connections = cursor.fetchone()[0]
        database_connections.set(active_connections)
```

### Backup and Recovery Procedures

#### Automated Backup Verification

**Backup Verification Script:**
```bash
#!/bin/bash
# verify_backup.sh

BACKUP_FILE="$1"
TEST_DB="resume_parser_test"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

echo "Verifying backup: $BACKUP_FILE"

# Create test database
psql -c "DROP DATABASE IF EXISTS $TEST_DB;"
psql -c "CREATE DATABASE $TEST_DB;"

# Restore backup to test database
if psql -d "$TEST_DB" < "$BACKUP_FILE"; then
    echo "✓ Backup restoration successful"
else
    echo "✗ Backup restoration failed"
    exit 1
fi

# Verify data integrity
ROW_COUNT=$(psql -d "$TEST_DB" -t -c "SELECT COUNT(*) FROM resumes_resume;")
if [ "$ROW_COUNT" -gt 0 ]; then
    echo "✓ Data verification successful ($ROW_COUNT resumes found)"
else
    echo "⚠ Warning: No resume data found in backup"
fi

# Check table structure
TABLE_COUNT=$(psql -d "$TEST_DB" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
echo "✓ Found $TABLE_COUNT tables in backup"

# Cleanup
psql -c "DROP DATABASE $TEST_DB;"

echo "Backup verification completed"
```

#### Recovery Testing

**Monthly Recovery Test:**
```bash
#!/bin/bash
# monthly_recovery_test.sh

TEST_DATE=$(date +"%Y%m%d")
TEST_DIR="/tmp/recovery_test_$TEST_DATE"
LOG_FILE="/var/log/recovery_test_$TEST_DATE.log"

echo "Starting monthly recovery test" | tee "$LOG_FILE"

# Create test environment
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Download latest backup
LATEST_BACKUP=$(aws s3 ls s3://your-backup-bucket/backups/ | sort | tail -n 1 | awk '{print $4}')
aws s3 cp "s3://your-backup-bucket/backups/$LATEST_BACKUP" . | tee -a "$LOG_FILE"

# Extract backup
tar -xzf "$LATEST_BACKUP" | tee -a "$LOG_FILE"

# Start test containers
docker-compose -f docker-compose.test.yml up -d | tee -a "$LOG_FILE"

# Wait for services to start
sleep 30

# Restore database
docker exec test_db psql -U postgres -c "CREATE DATABASE resume_parser_test;" | tee -a "$LOG_FILE"
docker exec -i test_db psql -U postgres -d resume_parser_test < backup_*/database.sql | tee -a "$LOG_FILE"

# Test application functionality
echo "Testing application endpoints..." | tee -a "$LOG_FILE"

# Health check
if curl -f http://localhost:8001/api/health/; then
    echo "✓ Health check passed" | tee -a "$LOG_FILE"
else
    echo "✗ Health check failed" | tee -a "$LOG_FILE"
    exit 1
fi

# Test file upload
if curl -X POST -F "file=@test_resume.pdf" http://localhost:8001/api/resumes/upload/; then
    echo "✓ File upload test passed" | tee -a "$LOG_FILE"
else
    echo "✗ File upload test failed" | tee -a "$LOG_FILE"
fi

# Test search functionality
if curl -X POST -H "Content-Type: application/json" \
        -d '{"query":"python"}' \
        http://localhost:8001/api/search/; then
    echo "✓ Search test passed" | tee -a "$LOG_FILE"
else
    echo "✗ Search test failed" | tee -a "$LOG_FILE"
fi

# Cleanup
docker-compose -f docker-compose.test.yml down | tee -a "$LOG_FILE"
rm -rf "$TEST_DIR"

echo "Recovery test completed. Check $LOG_FILE for details" | tee -a "$LOG_FILE"

# Send report
mail -s "Monthly Recovery Test Report" admin@yourdomain.com < "$LOG_FILE"
```

### FAQ

#### General Questions

**Q: What file formats are supported for resume uploads?**

A: The system supports the following file formats:
- PDF (.pdf)
- Microsoft Word (.doc, .docx)
- Rich Text Format (.rtf)
- Plain Text (.txt)

The maximum file size is 10MB by default, but this can be configured in the settings.

**Q: How accurate is the AI parsing?**

A: The AI parsing accuracy depends on several factors:
- File quality and format
- Resume structure and formatting
- AI provider (OpenAI GPT or Google Gemini)
- Language of the resume

Typically, the system achieves 85-95% accuracy for well-formatted resumes in English. You can always manually edit the extracted information if needed.

**Q: Can I use the system offline?**

A: The system requires internet connectivity for:
- AI processing (OpenAI/Google APIs)
- Cloud storage (if configured)
- Search functionality (if using cloud Elasticsearch)

However, QueryMind can work offline for file detection and basic processing, with uploads queued until connectivity is restored.

**Q: How is data privacy handled?**

A: The system implements several privacy measures:
- All data is encrypted in transit (HTTPS)
- Database encryption at rest
- Secure file storage with access controls
- AI providers process data according to their privacy policies
- Optional data retention policies
- GDPR compliance features

#### Technical Questions

**Q: Can I customize the AI parsing prompts?**

A: Yes, you can customize the AI parsing prompts by modifying the `ResumeParsingService` class:

```python
# apps/ai_parser/services.py
class ResumeParsingService:
    def get_parsing_prompt(self, text):
        return f"""
        Extract the following information from this resume:
        - Personal Information (name, email, phone, location)
        - Work Experience (company, position, dates, description)
        - Education (institution, degree, dates)
        - Skills (technical and soft skills)
        - Custom fields specific to your needs
        
        Resume text:
        {text}
        
        Return the information in JSON format.
        """
```

**Q: How do I add custom fields to the resume model?**

A: To add custom fields:

1. Update the model:
```python
# apps/resumes/models.py
class Resume(models.Model):
    # ... existing fields ...
    custom_field = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'resumes_resume'
```

2. Create and run migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Update the serializer:
```python
# apps/resumes/serializers.py
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'  # or list specific fields including custom_field
```

**Q: How do I configure multiple AI providers?**

A: You can configure multiple AI providers and implement fallback logic:

```python
# settings.py
AI_PROVIDERS = {
    'primary': {
        'type': 'openai',
        'api_key': 'your-openai-key',
        'model': 'gpt-4'
    },
    'fallback': {
        'type': 'google',
        'api_key': 'your-google-key',
        'model': 'gemini-pro'
    }
}

# apps/ai_parser/services.py
class ResumeParsingService:
    def parse_resume(self, file_path):
        try:
            return self._parse_with_provider('primary', file_path)
        except Exception as e:
            logger.warning(f"Primary provider failed: {e}")
            return self._parse_with_provider('fallback', file_path)
```

**Q: How do I scale the system for high volume?**

A: For high-volume deployments:

1. **Horizontal scaling:**
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 5
  
  worker:
    build: ./backend
    command: celery -A backend worker -l info
    deploy:
      replicas: 3
```

2. **Database optimization:**
```sql
-- Add read replicas
CREATE SUBSCRIPTION resume_parser_replica 
CONNECTION 'host=replica-host dbname=resume_parser user=replica_user' 
PUBLICATION resume_parser_pub;
```

3. **Caching strategy:**
```python
# Use Redis for caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis-cluster:6379/0',
    }
}
```

4. **Load balancing:**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

## API Documentation and Developer Guide

### API Overview

The Resume Parser system provides a comprehensive REST API for developers to integrate resume processing capabilities into their applications. The API follows RESTful principles and returns JSON responses.

**Base URL:** `http://localhost:8000/api/` (development) or `https://your-domain.com/api/` (production)

**Authentication:** The API uses token-based authentication for protected endpoints.

**Content Type:** All requests should use `Content-Type: application/json` unless uploading files.

### Authentication

#### Obtain Authentication Token

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### Using Authentication Token

Include the token in the Authorization header for protected endpoints:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Resume Management API

#### Upload Resume

```http
POST /api/resumes/upload/
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <resume_file>
source: "manual"  # optional: "manual" or "querymind"
```

**Response:**
```json
{
  "id": 123,
  "filename": "john_doe_resume.pdf",
  "file_size": 245760,
  "upload_timestamp": "2024-01-15T10:30:00Z",
  "processing_status": "pending",
  "source": "manual",
  "message": "Resume uploaded successfully. Processing started."
}
```

#### Get Resume List

```http
GET /api/resumes/
Authorization: Bearer <token>

# Query parameters:
# ?page=1&page_size=20&search=python&status=processed&source=manual
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/resumes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "filename": "john_doe_resume.pdf",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1-555-0123",
      "location": "New York, NY",
      "upload_timestamp": "2024-01-15T10:30:00Z",
      "processing_status": "completed",
      "ai_confidence_score": 0.92,
      "source": "manual",
      "tags": ["python", "django", "senior"]
    }
  ]
}
```

#### Get Resume Details

```http
GET /api/resumes/{id}/
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 123,
  "filename": "john_doe_resume.pdf",
  "file_size": 245760,
  "upload_timestamp": "2024-01-15T10:30:00Z",
  "processing_timestamp": "2024-01-15T10:31:30Z",
  "processing_status": "completed",
  "source": "manual",
  "ai_confidence_score": 0.92,
  "personal_info": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "location": "New York, NY",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe"
  },
  "work_experience": [
    {
      "company": "Tech Corp",
      "position": "Senior Software Engineer",
      "start_date": "2020-01-01",
      "end_date": "2024-01-01",
      "description": "Led development of web applications using Python and Django...",
      "location": "San Francisco, CA"
    }
  ],
  "education": [
    {
      "institution": "University of Technology",
      "degree": "Bachelor of Science in Computer Science",
      "start_date": "2016-09-01",
      "end_date": "2020-05-01",
      "gpa": "3.8",
      "location": "Boston, MA"
    }
  ],
  "skills": {
    "technical": ["Python", "Django", "JavaScript", "React", "PostgreSQL"],
    "soft": ["Leadership", "Communication", "Problem Solving"]
  },
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect",
      "issuer": "Amazon Web Services",
      "date": "2023-06-15",
      "expiry_date": "2026-06-15"
    }
  ],
  "languages": [
    {"language": "English", "proficiency": "Native"},
    {"language": "Spanish", "proficiency": "Intermediate"}
  ],
  "summary": "Experienced software engineer with 4+ years of experience...",
  "tags": ["python", "django", "senior"],
  "raw_text": "John Doe\nSoftware Engineer\n...",
  "file_url": "/api/resumes/123/download/"
}
```

#### Search API

```http
POST /api/search/
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "python django",
  "page": 1,
  "page_size": 20
}
```

**Response:**
```json
{
  "count": 45,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "results": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "score": 0.95,
      "highlights": {
        "skills": ["<em>Python</em>", "<em>Django</em>"],
        "experience": ["Developed web applications using <em>Python</em> and <em>Django</em>"]
      },
      "summary": "Senior Software Engineer with expertise in Python..."
    }
  ]
}
```

### System API

#### Health Check

```http
GET /api/health/
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time": 0.05
    },
    "elasticsearch": {
      "status": "healthy",
      "response_time": 0.12
    },
    "ai_service": {
      "status": "healthy",
      "provider": "openai",
      "response_time": 1.2
    }
  }
}
```

### Error Handling

#### Standard Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field_errors": {
        "email": ["Enter a valid email address"],
        "phone": ["Phone number is required"]
      }
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

#### HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server error

### Integration Examples

#### Python SDK Usage

```python
from resume_parser_sdk import ResumeParserClient

client = ResumeParserClient(
    base_url='http://localhost:8000/api/',
    token='your-jwt-token'
)

# Upload resume
with open('resume.pdf', 'rb') as f:
    result = client.upload_resume(f, source='manual')
    print(f"Resume uploaded with ID: {result['id']}")

# Search resumes
results = client.search_resumes(
    query='python django',
    filters={'experience_years': {'min': 3}}
)

for resume in results['results']:
    print(f"{resume['name']} - {resume['email']}")
```

#### JavaScript/React Integration

```javascript
import { ResumeParserClient } from 'resume-parser-sdk';

const client = new ResumeParserClient({
  baseURL: 'http://localhost:8000/api/',
  token: 'your-jwt-token'
});

// Upload resume
const handleFileUpload = async (file) => {
  try {
    const result = await client.uploadResume(file, { source: 'manual' });
    console.log(`Resume uploaded with ID: ${result.id}`);
  } catch (error) {
    console.error('Upload failed:', error.message);
  }
};

// Search resumes
const searchResumes = async (query) => {
  const results = await client.searchResumes({ query });
  return results.results;
};
```

### Rate Limiting

The API implements rate limiting:

- **Anonymous users:** 100 requests per hour
- **Authenticated users:** 1000 requests per hour
- **File uploads:** 50 uploads per hour per user

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
```

---

*This manual provides comprehensive guidance for installing, configuring, and using the Resume Parser system. Each section includes detailed instructions, examples, and troubleshooting tips to ensure successful deployment and operation.*