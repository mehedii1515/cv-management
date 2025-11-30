# Complete Folder & System Workflow Analysis

**Generated**: November 30, 2025  
**Repository**: cv-management  
**Analysis Scope**: Full project structure and system operations

---

## 📁 Complete Folder Structure Analysis

### **1. ROOT DIRECTORY** (`/`)

#### Configuration Files
```
.env                          → Environment variables (secrets)
.env.docker                   → Docker-specific configuration
.env.example                  → Template for .env
.gitignore                    → Git ignore rules
Caddyfile                     → Caddy reverse proxy config
docker-compose.yml           → Multi-container orchestration
docker-compose.simple.yml    → Simplified Docker setup
nginx.conf                    → Nginx reverse proxy config
render.yaml                   → Render deployment config
setup_database.sql           → PostgreSQL schema
```

#### Setup & Startup Scripts
```
setup.bat                     → Windows automatic setup
setup.sh                      → Linux/Mac automatic setup
start_servers.bat            → Windows start (backend + frontend)
start_servers.sh             → Linux/Mac start servers
start_production.bat         → Windows production startup
start_production.sh          → Linux/Mac production startup
stop_production.bat          → Windows stop production
stop_servers.sh              → Shutdown servers
switch-mode.sh               → Development/Production toggle
deploy-office.bat            → Office network deployment
manage-resume-parser.bat     → Resume parser management
```

#### Initialization & Utilities
```
install_libreoffice.sh       → Install LibreOffice (for .doc conversion)
create-ssl.sh                → Generate SSL certificates
test-deployment.bat          → Test deployment configuration
RUN_RESUME_PARSER.bat        → Quick start resume parser
```

#### Workflow Scripts
```
complete_workflow_demo.py    → End-to-end system demonstration
integration_manager.py       → QueryMind ↔ Search integration
querymind_search_integration.py → Alternative integration script
reparse_resume.py            → Reparse existing resumes
production_server.py         → Production server configuration
production_settings.py       → Production Django settings
production_requirements.txt  → Production dependencies
```

#### Database & Backup
```
export_database.bat          → Export PostgreSQL database
export_database_interactive.bat → Interactive database export
CREATE_POSTGRES_PORTABLE.bat → Create portable PostgreSQL
```

#### Documentation & Logs
```
README.md                    → Main project documentation
CODEBASE_ANALYSIS.md         → Detailed code analysis
DOCKER_SETUP.md             → Docker setup guide
docummentation/              → Complete documentation folder
logs/                        → Application logs
media/                       → User uploads directory
```

---

### **2. BACKEND** (`/backend/`)

Complete Django REST Framework application

#### Core Django Project
```
backend/
├── resume_parser/
│   ├── settings.py         → Main Django configuration
│   ├── production_settings.py → Production-specific settings
│   ├── urls.py             → URL routing (API endpoints)
│   ├── wsgi.py             → WSGI entry point
│   └── asgi.py             → ASGI entry point (WebSocket)
│
├── manage.py               → Django management CLI
├── requirements.txt        → Development dependencies
├── production_requirements.txt → Production dependencies
├── Dockerfile              → Container configuration
├── .dockerignore            → Docker ignore rules
└── .env                    → Backend environment variables
```

#### Applications (`/apps/`)

**A. RESUMES APP** (`apps/resumes/`)
```
Purpose: Resume CRUD operations and management

Files:
├── models.py              → Resume model (543 lines)
│   ├── Main Fields:
│   │   • UUID primary key
│   │   • Personal info (name, email, phone, DOB)
│   │   • Professional info (employer, experience, availability)
│   │   • Skills (JSON arrays)
│   │   • Education & certifications (JSON)
│   │   • File tracking (hash, path, type)
│   │   • Processing status (pending/processing/completed/failed)
│   │
│   ├── Methods:
│   │   • save() → Generate hashes & person IDs
│   │   • full_name property → Computed full name
│   │   • age property → Calculate from DOB
│   │   • experience_display property → Format experience
│   │
│   └── Indexes (11 total):
│       • content_hash (duplicate detection)
│       • person_soft_id (person matching)
│       • email, cv_hash, name, experience, location, timestamp
│
├── views.py               → API endpoints (978 lines)
│   ├── ResumePagination → Custom pagination (10 per page, max 50)
│   ├── ResumeFilter → Advanced filtering with OR logic
│   ├── ResumeViewSet → CRUD endpoints
│   │   • GET /api/resumes/ → List all
│   │   • POST /api/resumes/ → Create
│   │   • GET /api/resumes/{id}/ → Get single
│   │   • DELETE /api/resumes/{id}/ → Delete
│   │   • POST /api/resumes/upload/ → Upload & parse
│   │   • GET /api/resumes/{id}/parsed-data/ → Get parsed data
│   │   • POST /api/resumes/{id}/reparse/ → Reparse
│   │
│   └── Filters:
│       • Location (OR logic for multiple)
│       • Expertise areas (JSON search)
│       • Sectors (JSON search)
│       • Skills (JSON search)
│       • Experience range (gte/lte)
│
├── serializers.py         → Data serialization
│   ├── ResumeSerializer → Main serialization
│   ├── ResumeUploadSerializer → Single file upload
│   └── BatchResumeUploadSerializer → Multiple file upload
│
├── admin.py              → Django admin configuration
│   ├── ResumeAdmin
│   │   • List display (name, email, employer, experience, status)
│   │   • Filters (status, location, experience)
│   │   • Search fields (name, email, employer)
│   │   • Readonly fields (hash, timestamp, computed fields)
│   │   • Custom fieldsets for organization
│   │
│   └── Pretty print for JSON fields
│
├── urls.py               → URL patterns
│   └── router.register() → Auto-generate CRUD routes
│
├── apps.py               → App configuration
├── __init__.py           → Package init
└── migrations/           → Database migrations
    ├── 0001_initial.py
    ├── 0002_*
    ├── 0003_*
    ├── 0004_expertise_details
    └── 0005_workexperience
```

**B. AI PARSER APP** (`apps/ai_parser/`)
```
Purpose: AI-powered resume parsing and data extraction

Files:
├── services.py           → Main parsing service (1122 lines)
│   ├── ResumeParsingService class
│   │   • __init__() → Initialize OpenAI/Gemini clients
│   │   • parse_resume() → Main parsing logic
│   │   • extract_data() → Extract specific fields
│   │   • validate_extracted_data() → Quality check
│   │   • get_extraction_prompt() → Generate AI prompt
│   │   • handle_parsing_errors() → Error recovery
│   │
│   ├── AI Provider Support:
│   │   • OpenAI GPT-4 / GPT-3.5-turbo (primary)
│   │   • Google Gemini (fallback)
│   │   • Automatic provider switching on failure
│   │
│   ├── Features:
│   │   • Token counting (tiktoken)
│   │   • Response validation
│   │   • Error logging & recovery
│   │   • Cost optimization
│   │   • Batch processing support
│   │
│   └── Error Handling:
│       • API timeout handling
│       • Rate limit management
│       • Fallback mechanism
│
├── unstructured_service.py → Document extraction
│   ├── UnstructuredService class
│   │   • extract_text() → Extract from any format
│   │   • parse_pdf() → PDF processing
│   │   • parse_docx() → Word document parsing
│   │   • parse_doc() → Legacy DOC files
│   │   • extract_tables() → Table detection
│   │   • extract_sections() → Section detection
│   │
│   ├── Supported Formats:
│   │   • PDF (with Poppler for text extraction)
│   │   • DOCX (native XML parsing)
│   │   • DOC (via conversion)
│   │   • RTF (text extraction)
│   │   • TXT (direct parsing)
│   │
│   ├── Features:
│   │   • OCR for scanned documents (Tesseract)
│   │   • Multi-language support
│   │   • High-resolution extraction
│   │   • Table & section detection
│   │   • Contact info extraction
│   │
│   └── Quality Indicators:
│       • Extraction confidence
│       • Character count
│       • Format detection
│
├── gemini_service.py     → Google Gemini integration
│   ├── GeminiService class
│   │   • initialize() → Setup API connection
│   │   • extract_resume_data() → Main extraction
│   │   • parse_json_response() → Parse AI response
│   │   • handle_errors() → Error management
│   │
│   ├── Configuration:
│   │   • Model: Gemini 1.5 Pro
│   │   • Free API access
│   │   • Token limits
│   │   • Rate limiting
│   │
│   └── Use Cases:
│       • Fallback from OpenAI
│       • Non-English documents
│       • Cost-sensitive processing
│
├── doc_converter.py      → Document format conversion
│   ├── DocConverter class
│   │   • convert_doc_to_docx() → Legacy document conversion
│   │   • convert_to_text() → Any format to text
│   │   • detect_format() → Auto-detect file type
│   │
│   └── Requirements:
│       • LibreOffice (for .doc conversion)
│       • Poppler (for PDF handling)
│
├── views.py              → API endpoints
│   ├── @api_view endpoints:
│   │   • GET /api/ai-parser/test-openai/ → Connection test
│   │   • GET /api/ai-parser/test-unstructured/ → Capability test
│   │   • POST /api/ai-parser/extract/ → Extract from text
│   │   • POST /api/ai-parser/test-gemini/ → Gemini test
│   │
│   └── Response Format:
│       • status: success/error
│       • data: extracted information
│       • errors: validation errors
│
├── urls.py               → URL patterns
├── apps.py               → App configuration
└── __init__.py           → Package init
```

**C. SEARCH APP** (`apps/search/`)
```
Purpose: Elasticsearch full-text search & indexing

Files:
├── services.py           → Search service (348 lines)
│   ├── SearchService class
│   │   • __init__() → Initialize Elasticsearch client
│   │   • test_connection() → Verify ES connectivity
│   │   • create_index() → Setup search indices
│   │   • search_documents() → Main search method
│   │   • boolean_search() → DTSearch-style operators (AND/OR/NOT)
│   │   • advanced_search() → Multi-criteria search
│   │   • get_suggestions() → Autocomplete suggestions
│   │   • reindex_database() → Full reindexing
│   │   • delete_document() → Remove from index
│   │
│   ├── Search Features:
│   │   • Full-text search across resume content
│   │   • Boolean operators (AND, OR, NOT)
│   │   • Field-specific search
│   │   • Filters (date, file type, size)
│   │   • Pagination (max 100 per page)
│   │   • Result ranking & scoring
│   │   • 5-minute cache for queries
│   │
│   └── Performance:
│       • Query optimization
│       • Index segmentation
│       • Cache layer
│       • Bulk operations
│
├── documents.py          → Elasticsearch mapping
│   ├── CVDocument class
│   │   • Document structure definition
│   │   • Field mappings
│   │   • Analyzers configuration
│   │
│   ├── Fields Indexed:
│   │   • id (UUID)
│   │   • full_name (text with analyzer)
│   │   • email (keyword)
│   │   • phone (text)
│   │   • location (keyword)
│   │   • skills (array)
│   │   • experience (text)
│   │   • education (text)
│   │   • expertise_areas (keyword array)
│   │   • sectors (keyword array)
│   │   • years_of_experience (integer)
│   │   • timestamp (date)
│   │
│   └── Analyzers:
│       • standard_analyzer: Tokenization + lowercasing
│       • email_analyzer: Email-specific
│       • skill_analyzer: Skill-specific
│
├── documents_*.py        → Versioned document definitions
│   ├── documents_old.py  → Legacy mapping
│   ├── documents_new.py  → Experimental mapping
│   └── file_documents*.py → File indexing variants
│
├── file_search_service.py → File-specific search
│   ├── FileSearchService class
│   │   • index_file_content() → Index file directly
│   │   • search_files() → Search within files
│   │   • extract_file_metadata() → File properties
│   │   • cache_file_index() → Performance optimization
│   │
│   └── Use Cases:
│       • Direct file search (DTSearch-like)
│       • File content indexing
│       • Metadata search
│
├── signals.py            → Django post-save signals (123 lines)
│   ├── index_cv_on_save() → Auto-index on CV save
│   │   • Trigger on Resume save
│   │   • Check if processed
│   │   • Queue async indexing tasks
│   │   • Update file indices
│   │
│   ├── Celery Tasks:
│   │   • index_single_cv.apply_async()
│   │   • index_resume_file.apply_async()
│   │
│   └── Signal Handlers:
│       • post_save signal (indexing)
│       • post_delete signal (cleanup)
│       • Async processing via Celery
│
├── tasks.py              → Celery background tasks
│   ├── index_single_cv.apply_async() → Index one CV
│   ├── index_resume_file.apply_async() → Index file
│   ├── bulk_reindex() → Batch indexing
│   └── cleanup_indices() → Index maintenance
│
├── views.py              → API endpoints (402 lines)
│   ├── @api_view endpoints:
│   │   • GET /api/search/?q=... → Basic search
│   │   • GET /api/search/boolean/?q=... → Boolean search
│   │   • POST /api/search/advanced/ → Advanced search
│   │   • GET /api/search/suggest/?q=... → Suggestions
│   │   • POST /api/search/reindex/ → Force reindex
│   │   • GET /api/search/status/ → System status
│   │
│   └── Query Parameters:
│       • q: Search query
│       • page: Page number (default: 1)
│       • size: Results per page (max: 100)
│       • filters: JSON filter object
│
├── models.py             → Search metadata models
├── admin.py              → Django admin config
├── urls.py               → URL patterns
├── apps.py               → App configuration
├── migrations/           → Database migrations
├── management/           → Management commands
│   └── commands/
│       └── reindex_files.py → Reindex management command
│           • --all: Reindex all documents
│           • --batch-size: Batch size
│           • --index: Specific index
│           • Progress reporting
│           • Error handling
│
├── tests.py              → Test cases
└── __init__.py           → Package init
```

**D. CORE APP** (`apps/core/`)
```
Purpose: Shared utilities and middleware

Files:
├── views.py              → API views
│   ├── HealthCheck endpoint
│   ├── System status endpoint
│   └── Utility views
│
├── health.py             → Health check service
│   ├── check_database() → DB connectivity
│   ├── check_elasticsearch() → ES status
│   ├── check_redis() → Cache availability
│   └── overall_health() → Aggregate status
│
├── urls.py               → URL patterns
│   └── /api/health/ → Health check endpoint
│
├── apps.py               → App configuration
└── __init__.py           → Package init
```

#### Database & Storage
```
backend/
├── db.sqlite3            → Development database (SQLite)
├── media/                → User uploads
│   └── uploads/          → Resume files
├── staticfiles/          → Collected static files
├── logs/                 → Application logs
└── poppler-24.08.0/      → PDF processing library
```

#### Virtual Environment
```
backend/
└── venv/                 → Python virtual environment
    ├── lib/              → Installed packages
    ├── Scripts/ (Windows)
    └── bin/ (Linux/Mac)
```

---

### **3. FRONTEND** (`/frontend/`)

Next.js React application

#### Application Structure
```
frontend/
├── src/
│   ├── app/              → Next.js App Router pages
│   │   ├── page.tsx      → Dashboard (399 lines)
│   │   │   • Main interface
│   │   │   • Tab navigation (#resumes, #upload, #dtsearch, #filesearch)
│   │   │   • Resume management
│   │   │   • Upload zone
│   │   │   • Search interface
│   │   │   • Statistics display
│   │   │   • State management
│   │   │
│   │   ├── layout.tsx    → Root layout
│   │   ├── upload/       → Upload page
│   │   ├── search/       → Search page
│   │   ├── results/      → Results display
│   │   └── admin/        → Admin interface
│   │
│   ├── components/       → React components
│   │   ├── ui/           → Shadcn/UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Dialog.tsx
│   │   │   ├── Tabs.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Separator.tsx
│   │   │   └── (15+ more UI components)
│   │   │
│   │   ├── forms/        → Form components
│   │   │   ├── FormField.tsx
│   │   │   ├── FormInput.tsx
│   │   │   ├── FormSelect.tsx
│   │   │   └── FormValidation.tsx
│   │   │
│   │   ├── layout/       → Layout components
│   │   │   ├── Breadcrumb.tsx
│   │   │   ├── PageHeader.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Header.tsx
│   │   │
│   │   ├── FileUploadZone.tsx
│   │   ├── ResumeCard.tsx
│   │   ├── StatsCards.tsx
│   │   ├── SearchFilters.tsx
│   │   ├── DTSearchPanel.tsx
│   │   ├── FileSearchPanel.tsx
│   │   ├── EnhancedFileViewer.tsx
│   │   └── (20+ feature components)
│   │
│   ├── hooks/            → Custom React hooks
│   │   ├── useResumes.ts → Resume management hook
│   │   ├── useSearch.ts → Search hook
│   │   ├── useAuth.ts → Authentication hook
│   │   └── (custom hooks for features)
│   │
│   ├── lib/              → Utility functions
│   │   ├── api.ts → API client configuration
│   │   │   • Base URL: http://localhost:8000/api
│   │   │   • Timeout: 30 seconds
│   │   │   • Retry logic: 3 attempts
│   │   │   • Error interceptor
│   │   │   • Token management
│   │   │
│   │   ├── utils.ts → Helper functions
│   │   └── constants.ts → Constants
│   │
│   └── types/            → TypeScript types
│       ├── Resume.ts
│       ├── API.ts
│       ├── filters.ts
│       └── (domain types)
│
├── public/               → Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
│
├── package.json          → Node dependencies
│   ├── name: resume-parser-frontend
│   ├── version: 1.0.0
│   │
│   ├── Dependencies (26 total):
│   │   • next@14.0.4 → React framework
│   │   • react@18.2.0 → UI library
│   │   • @radix-ui/* → Component primitives
│   │   • tailwindcss → Utility CSS
│   │   • react-hook-form → Form management
│   │   • zod → Validation
│   │   • axios → HTTP client
│   │   • recharts → Data visualization
│   │   • react-dropzone → File upload
│   │
│   ├── Scripts:
│   │   • "dev": "next dev -H 0.0.0.0" → Development server
│   │   • "build": "next build" → Production build
│   │   • "start": "next start" → Production server
│   │   • "lint": "next lint" → Code linting
│
├── tsconfig.json         → TypeScript configuration
├── tailwind.config.js    → Tailwind CSS config
├── postcss.config.js     → PostCSS config
├── next.config.js        → Next.js configuration
├── components.json       → Shadcn/UI config
├── .env                  → Environment variables
└── .gitignore            → Git ignore rules
```

#### Frontend Data Flow
```
User Interaction
    ↓
Component (e.g., page.tsx)
    ↓
Custom Hook (e.g., useResumes.ts)
    ↓
API Client (lib/api.ts)
    ↓
HTTP Request to Backend
    ↓
Backend Response
    ↓
State Update (useState)
    ↓
Component Re-render
    ↓
UI Update
```

---

### **4. QUERYMIND** (`/QueryMind/`)

CV Detection & Classification Engine

#### Core Processing
```
QueryMind/
├── main.py               → Main processing workflow (386 lines)
│   ├── Workflow:
│   │   1. Load configuration
│   │   2. Load previously processed files
│   │   3. Scan source directory
│   │   4. For each file:
│   │      a. Extract text
│   │      b. Tokenize (max 500 tokens)
│   │      c. AI classification (IsResume?)
│   │      d. If resume, upload to backend
│   │      e. Log processing result
│   │   5. Generate output files
│   │
│   ├── Key Functions:
│   │   • load_processed_files() → Load tracking
│   │   • save_processed_files() → Update tracking
│   │   • Tokenize_Data() → Token truncation
│   │   • AI_Extract_Data() → OpenAI call
│   │   • IsResume_With_Confidence() → Classification
│   │   • send_cv_to_resume_parser() → Upload to backend
│   │
│   ├── Configuration:
│   │   • SOURCE_FOLDER = Network drive path
│   │   • RESUME_PARSER_URL = http://localhost:8000
│   │   • INTEGRATION_ENABLED = True/False
│   │   • BATCH_SIZE = 1000 files
│   │
│   └── Output:
│       • tokens.json → Token counts
│       • Resume_Classification.xlsx → Results
│
├── enhanced_main.py      → Enhanced version with improvements
│   • Better error handling
│   • Additional logging
│   • Performance optimizations
│   • Batch processing enhancements
│
├── integration_manager.py → Integration control
│   ├── IntegratedCVProcessor class
│   │   • scan_for_new_files()
│   │   • process_batch()
│   │   • update_elasticsearch()
│   │   • track_processing()
│   │
│   └── Interactive Menu:
│       1. Scan for new files once
│       2. Start continuous monitoring
│       3. Process specific file
│       4. View integration status
│
├── cv_monitoring_service.py → File monitoring
│   ├── CVMonitoringService class
│   │   • watch_directory()
│   │   • detect_new_files()
│   │   • classify_files()
│   │   • auto_upload()
│   │
│   └── Features:
│       • Real-time file detection
│       • Automatic classification
│       • Auto-upload on detection
│       • Statistics tracking
│
├── Include/              → Shared utilities
│   ├── Config.py        → Configuration
│   │   • GPT_MODEL = "gpt-3.5-turbo"
│   │   • DATA_FOLDER = "Sample CVs\\"
│   │   • OUTPUT_FOLDER = "Output\\"
│   │   • InitialiseAPI() → Load API key
│   │
│   ├── Filestream.py    → File operations
│   │   • Read file content
│   │   • Convert formats (.doc to .docx)
│   │   • Handle errors
│   │   • Track files
│   │
│   └── misc.py          → Miscellaneous utilities
│
├── processed_files.txt  → Tracking log
│   • List of processed file paths
│   • One path per line
│   • Used to prevent reprocessing
│
├── requirements.txt     → Python dependencies
│   • openai
│   • requests
│   • pandas
│   • python-dotenv
│   • tiktoken
│
├── tests/               → Test files
│   ├── test_watcher.py
│   ├── test_doc_conversion.py
│   └── debug_*.py
│
├── FILE_WATCHER_GUIDE.md → Documentation
├── QUERYMIND_QUICK_START.md
├── README.md
└── watcher_config.py    → File watcher configuration
```

#### QueryMind Architecture Diagram
```
┌─────────────────────────────────────┐
│   QueryMind Main Process            │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   Initialize Configuration          │
│  - Load API keys                    │
│  - Load processed files tracking    │
│  - Connect to backend API           │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   Scan Source Directory             │
│  - Find all resume files            │
│  - Filter by type                   │
│  - Check against processed list     │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   For Each File (Batch Processing)  │
└─────────────────────────────────────┘
            ↓
        ┌───┴───┐
        │       │
        ↓       ↓
    ┌────────────────────────┐
    │ Extract Text           │
    │ (Unstructured)         │
    └────────────────────────┘
            ↓
    ┌────────────────────────┐
    │ Tokenize (Max 500)     │
    │ (tiktoken)             │
    └────────────────────────┘
            ↓
    ┌────────────────────────┐
    │ AI Classification      │
    │ (OpenAI GPT-3.5)       │
    │ "Is this a resume?"    │
    └────────────────────────┘
            ↓
        ┌───┴───┐
        │ Yes   │ No → Log & Skip
        │       │
        ↓       
    ┌────────────────────────┐
    │ Convert Format         │
    │ (.doc → .docx)         │
    └────────────────────────┘
            ↓
    ┌────────────────────────┐
    │ POST to Backend API    │
    │ /api/resumes/upload/   │
    └────────────────────────┘
            ↓
        ┌───┴───┐
        │       │
    Success  Error → Retry/Log
        │       │
        ↓
    ┌────────────────────────┐
    │ Track in processed_*   │
    │ Log statistics         │
    └────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   Generate Output                   │
│  - tokens.json                      │
│  - Resume_Classification.xlsx       │
│  - Statistics report                │
└─────────────────────────────────────┘
```

---

### **5. DOCUMENTATION** (`/docummentation/`)

Comprehensive guides and references

```
docummentation/
├── README.md                    → Original documentation
├── SETUP_GUIDE.md              → Installation guide
├── USER_MANUAL.md              → User guide (4800+ lines)
├── DEPLOYMENT_GUIDE.md         → Deployment instructions
├── PRODUCTION_DEPLOYMENT_GUIDE.md
├── POSTGRESQL_SETUP.md         → Database setup
├── DOCX_PDF_CONVERSION_SETUP.md
├── FILE_INDEX_SEARCH_GUIDE.md  → Search documentation
├── FIREWALL_SETUP_PC.md        → Network setup
├── USER_INSTRUCTIONS.md        → Step-by-step instructions
├── OFFICE_ACCESS_GUIDE.md      → Office network access
├── setup.md                    → Alternative setup
├── BATCH_UPLOAD_FEATURE.md     → Batch upload guide
├── SECTORS_OR_FILTER_FEATURE.md
├── DTSEARCH_FRONTEND_INTEGRATION.md
├── DEPLOYMENT_COMPLETE.md
├── DEPLOYMENT_CHECKLIST.md
├── PURE_FILE_SEARCH_SYSTEM.md
└── dtSearch_Desktop.pdf        → DTSearch documentation
```

---

### **6. LOGS** (`/logs/`)

Application and system logs

```
logs/
├── django.log           → Django application logs
├── celery.log          → Background task logs
├── elasticsearch.log   → Search engine logs
├── integration.log     → QueryMind integration logs
└── error.log           → Error tracking
```

---

### **7. MEDIA** (`/media/`)

User uploads and static files

```
media/
├── uploads/            → Resume files directory
│   ├── *.pdf           → Uploaded PDF files
│   ├── *.docx          → Word documents
│   ├── *.doc           → Legacy Word files
│   ├── *.txt           → Text files
│   └── *.rtf           → Rich text files
```

---

## 🔄 Complete System Workflow

### **MAIN SYSTEM ARCHITECTURE**

```
┌──────────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                              │
│  Next.js Frontend (React, TypeScript, Tailwind CSS, shadcn/ui)       │
│  Port: 3000                                                           │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            │     HTTP/REST Requests         │
            │                                 │
            │  - JSON payloads                │
            │  - Authentication tokens        │
            │  - Multipart file uploads       │
            │                                 │
            ↓
┌──────────────────────────────────────────────────────────────────────┐
│                    API GATEWAY LAYER                                  │
│  Django REST Framework                                               │
│  Port: 8000                                                          │
├──────────────────────────────────────────────────────────────────────┤
│ • CORS Middleware (Allow frontend requests)                          │
│ • Authentication (Django session/JWT)                                │
│ • Rate Limiting & Throttling                                         │
│ • Request/Response Logging                                           │
│ • Error Handling & Validation                                        │
└────┬─────────────────────────────────────────────────────┬───────────┘
     │                                                      │
     ├──────────────────────┬──────────────────┬──────────┤
     │                      │                  │          │
     ↓                      ↓                  ↓          ↓
┌─────────────┐  ┌────────────────┐  ┌──────────────┐  ┌───────────┐
│  Resume     │  │ AI Parser      │  │ Search       │  │ Core      │
│  Management │  │ Service        │  │ Service      │  │ Service   │
│             │  │                │  │              │  │           │
│ CRUD Ops    │  │ • OpenAI       │  │ • Index CV   │  │ • Health  │
│ Filtering   │  │ • Gemini       │  │ • Full-text  │  │ • Utils   │
│ Pagination  │  │ • Unstructured │  │ • Boolean    │  │ • Auth    │
│ Upload      │  │ • Conversion   │  │ • Advanced   │  │           │
└──────┬──────┘  └────────┬───────┘  └──────┬───────┘  └───────────┘
       │                  │                 │
       │ Signals          │ Async Tasks     │
       └──────────────────┼─────────────────┘
                          │
                          ↓
            ┌─────────────────────────────┐
            │   Task Queue (Celery)       │
            │                             │
            │ • Background processing     │
            │ • Async indexing           │
            │ • Scheduled tasks          │
            │ • Job status tracking       │
            └──────┬──────────────────────┘
                   │
        ┌──────────┴───────────┐
        │                      │
        ↓                      ↓
    ┌──────────┐          ┌──────────┐
    │  Redis   │          │ Celery   │
    │  Cache   │          │ Workers  │
    │          │          │          │
    │ • Sessions          │ • Process
    │ • Query cache       │ • Index
    │ • Rate limits       │ • Convert
    └──────────┘          └──────────┘
        │
        ↓
┌──────────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │  SQLite/        │    │  Elasticsearch   │    │  File        │  │
│  │  PostgreSQL     │    │  Search Index    │    │  Storage     │  │
│  │                 │    │                  │    │              │  │
│  │ • Resumes       │    │ • CV documents   │    │ • Uploads    │  │
│  │ • Users         │    │ • Full-text idx  │    │ • Media      │  │
│  │ • Metadata      │    │ • Field mapping  │    │ • Static     │  │
│  │ • Transactions  │    │ • Aggregations   │    │              │  │
│  │                 │    │ • Faceting       │    │              │  │
│  └─────────────────┘    └──────────────────┘    └──────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 END-TO-END WORKFLOW

### **WORKFLOW 1: Manual Resume Upload**

```
1. USER UPLOADS FILE
   └─ Browser: Drag-drop or select file
   └─ FileUploadZone component

2. FRONTEND VALIDATION
   └─ File type check (.pdf, .docx, etc.)
   └─ File size check (< 10MB)
   └─ Display preview

3. UPLOAD REQUEST
   └─ Frontend: POST /api/resumes/upload/
   └─ Multipart form data with file
   └─ Content-Type: multipart/form-data

4. BACKEND RECEIVES FILE
   └─ ResumeUploadSerializer validates
   └─ File saved to media/uploads/

5. DOCUMENT EXTRACTION
   └─ UnstructuredService.extract_text()
   └─ Select appropriate extractor (PDF/DOCX/DOC/etc.)
   └─ Return raw text

6. AI PARSING
   └─ ResumeParsingService.parse_resume()
   └─ Send text to OpenAI GPT
   └─ Extract: name, email, skills, experience, etc.
   └─ Fallback to Gemini if OpenAI fails

7. DATA VALIDATION
   └─ Validate extracted data structure
   └─ Check required fields
   └─ Normalize data formats

8. DATABASE STORAGE
   └─ Create Resume model instance
   └─ Generate hashes (cv_hash, content_hash, person_soft_id)
   └─ Check for duplicates
   └─ Save to database

9. POST-SAVE SIGNAL TRIGGERED
   └─ apps/search/signals.py
   └─ index_cv_on_save() signal fires
   └─ Queue Celery task: index_single_cv

10. ASYNC ELASTICSEARCH INDEXING
    └─ Celery worker picks up task
    └─ SearchService.search_documents() prepares index
    └─ Elasticsearch receives document
    └─ Index created/updated

11. RESPONSE TO FRONTEND
    └─ HTTP 201 Created
    └─ JSON response with resume data
    └─ Resume ID for future reference

12. FRONTEND UPDATE
    └─ Display success message
    └─ Update resume list
    └─ Clear upload form
    └─ Show resume card
```

### **WORKFLOW 2: Search for Resume**

```
1. USER ENTERS SEARCH QUERY
   └─ Frontend: Type in search box
   └─ Example: "Python Django Developer"

2. FRONTEND EXECUTES SEARCH
   └─ GET /api/search/?q=Python+Django+Developer
   └─ Optional: Add filters (location, skills, etc.)
   └─ Pass pagination (page, page_size)

3. BACKEND PROCESSES QUERY
   └─ SearchService.search_documents()
   └─ Parse query string
   └─ Build filter criteria
   └─ Check cache first (5-minute TTL)

4. ELASTICSEARCH QUERY EXECUTION
   └─ Create DSL query (Q object)
   └─ Apply field weights (name more important than location)
   └─ Apply filters (if provided)
   └─ Execute search
   └─ Calculate relevance scores

5. RESULT PROCESSING
   └─ Format results JSON
   └─ Add metadata (total hits, query time)
   └─ Add pagination info
   └─ Sort by relevance score

6. CACHE RESULT
   └─ Store in Redis for 5 minutes
   └─ Key: hash(query + filters)

7. RESPONSE TO FRONTEND
   └─ HTTP 200 OK
   └─ JSON with:
   │  ├─ hits: [array of matching resumes]
   │  ├─ total: 42
   │  ├─ pagination: {page: 1, has_next: true}
   │  └─ search_info: {query, time_ms}

8. FRONTEND DISPLAYS RESULTS
   └─ Map results to ResumeCard components
   └─ Show pagination controls
   └─ Enable infinite scroll (optional)
   └─ Highlight matching terms

9. USER CLICKS ON RESULT
   └─ Navigate to resume detail page
   └─ GET /api/resumes/{id}/
   └─ Display full resume information
```

### **WORKFLOW 3: QueryMind Batch Processing**

```
1. INITIALIZE QUERYMIND
   └─ python QueryMind/main.py
   └─ Load configuration
   └─ Initialize OpenAI client
   └─ Load processed files tracking

2. SCAN DIRECTORY
   └─ Connect to network drive
   └─ Scan: \\server\MSL-DATA\PROJECTS\...
   └─ Find all resume files
   └─ Filter out already processed

3. BATCH PROCESSING (size: 1000)
   For each file in batch:
   
   a) Extract text
      └─ Use Unstructured library
      └─ Auto-detect format (PDF, DOCX, DOC, TXT, RTF)
      └─ Return raw text
   
   b) Tokenize (max 500 tokens)
      └─ Use tiktoken encoder
      └─ Truncate if necessary
      └─ Prepare for AI processing
   
   c) AI Classification
      └─ Send to OpenAI GPT-3.5-turbo
      └─ System prompt: "Is this a resume?"
      └─ Receive response: "Yes" or "No"
   
   d) If Resume Detected:
      └─ Format for upload
      └─ Convert .doc to .docx (if needed)
      └─ POST to /api/resumes/upload/
      └─ Receive resume ID
   
   e) Track Processing
      └─ Add to processed_files.txt
      └─ Log success/failure
      └─ Update statistics

4. GENERATE OUTPUT
   └─ Create tokens.json (token counts)
   └─ Create Resume_Classification.xlsx (results)
   └─ Display statistics:
      ├─ Files scanned: 100
      ├─ Resumes found: 75
      ├─ Uploaded: 73
      ├─ Success rate: 97.3%
      └─ Processing time: 145 seconds

5. ELASTICSEARCH AUTO-INDEXING
   └─ Each uploaded resume triggers signal
   └─ Celery task queued for indexing
   └─ Background worker indexes document
   └─ Resumes become searchable
```

### **WORKFLOW 4: System Health Check**

```
1. FRONTEND REQUESTS STATUS
   └─ GET /api/health/

2. CORE APP CHECKS ALL SYSTEMS
   └─ check_database()
      ├─ Connect to SQLite/PostgreSQL
      └─ Return: connected/failed
   
   └─ check_elasticsearch()
      ├─ Connect to ES cluster
      ├─ Check indices exist
      └─ Return: connected/failed
   
   └─ check_redis()
      ├─ Connect to Redis
      ├─ Test ping
      └─ Return: connected/failed
   
   └─ check_openai()
      ├─ Test API connection
      └─ Return: connected/failed
   
   └─ check_gemini()
      ├─ Test API connection
      └─ Return: connected/failed

3. AGGREGATE STATUS
   └─ overall_health = all_systems_ok
   └─ Return detailed status

4. FRONTEND DISPLAYS HEALTH
   └─ Show dashboard with indicators
   └─ Green = operational
   └─ Yellow = degraded
   └─ Red = down
```

---

## 📊 Data Flow Through System

### **Complete Data Journey**

```
File Upload
    ↓
    ├─→ Browser (FileUploadZone)
    │       ↓
    │       Validation (type, size)
    │       ↓
    │       POST /api/resumes/upload/
    │       ↓
    ├─→ Django Backend
    │       ↓
    │       ResumeUploadSerializer
    │       ↓
    │       File saved to media/uploads/
    │       ↓
    │       UnstructuredService.extract_text()
    │       ↓
    ├─→ Text Extraction
    │       ├─→ Poppler (PDF)
    │       ├─→ XML Parser (DOCX)
    │       ├─→ LibreOffice (DOC)
    │       └─→ Direct read (TXT/RTF)
    │       ↓
    ├─→ AI Parser Service
    │       ├─→ OpenAI GPT
    │       │   └─ If fails → Fallback to Gemini
    │       │
    │       ├─→ Google Gemini (Fallback)
    │       │   └─ Cost-free alternative
    │       │
    │       └─ Extract structured JSON
    │           ├─ Name, email, phone
    │           ├─ Skills, experience
    │           ├─ Education, certifications
    │           └─ etc.
    │       ↓
    ├─→ Database Storage
    │       ├─ Create Resume record
    │       ├─ Calculate hashes
    │       ├─ Check duplicates
    │       └─ Save to database
    │       ↓
    ├─→ Post-Save Signal
    │       └─ Trigger Elasticsearch indexing
    │       ↓
    ├─→ Background Task (Celery)
    │       ├─ SearchService prepares document
    │       ├─ CVDocument mapping applied
    │       └─ Send to Elasticsearch
    │       ↓
    ├─→ Elasticsearch Indexing
    │       ├─ Parse document
    │       ├─ Tokenize text
    │       ├─ Create inverted index
    │       └─ Store in indices
    │       ↓
    └─→ Search Ready
        └─ Now available for search queries
            └─ Full-text search
            └─ Boolean search
            └─ Advanced filtering
```

---

## 🎯 Key Integration Points

### **1. QueryMind → Backend Integration**

```
QueryMind sends:
  POST /api/resumes/upload/
  {
    "file": <multipart file>,
    "source": "querymind",
    "metadata": {
      "scan_date": "2025-11-30",
      "batch_id": "batch_001"
    }
  }

Backend processes and returns:
  {
    "id": "uuid-123",
    "status": "success",
    "message": "Resume processed",
    "parsed_data": {
      "first_name": "John",
      "last_name": "Smith",
      ...
    }
  }
```

### **2. Django → Elasticsearch Integration**

```
Signal Flow:
  Resume.save()
    ↓
  post_save signal fires
    ↓
  index_cv_on_save() handler
    ↓
  Check if processed
    ↓
  Queue Celery task
    ↓
  index_single_cv.apply_async()
    ↓
  Celery worker executes
    ↓
  SearchService.create_index()
    ↓
  CVDocument mapping
    ↓
  Elasticsearch receives document
    ↓
  Resume indexed and searchable
```

### **3. Frontend → Backend API Integration**

```
Frontend Request:
  GET /api/resumes/
  Headers: {
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
  }

Backend Response:
  {
    "count": 142,
    "next": "http://.../page=2",
    "results": [
      {resume objects},
      ...
    ]
  }

Frontend renders:
  ResumeCard components
  Pagination controls
  Filter UI
```

---

## 🔧 System Dependencies & Interactions

```
┌─ OpenAI GPT ──────┐
│                    │
│  ├─ API Key        │
│  ├─ Model: GPT-3.5 │
│  └─ Max tokens: 8K │
│                    │
└─→ AI Parser Service

┌─ Google Gemini ────┐
│                    │
│  ├─ Free API       │
│  ├─ Fallback       │
│  └─ Non-English    │
│                    │
└─→ AI Parser Service (Fallback)

┌─ Unstructured ─────┐
│                    │
│  ├─ PDF extract    │
│  ├─ DOCX parse     │
│  ├─ Table detect   │
│  └─ OCR (Tesseract)│
│                    │
└─→ Text Extraction

┌─ Poppler ──────────┐
│                    │
│  ├─ PDF → Text     │
│  └─ Layout aware   │
│                    │
└─→ PDF Processing

┌─ Elasticsearch ────┐
│                    │
│  ├─ Full-text idx  │
│  ├─ Analyzers      │
│  └─ Aggregations   │
│                    │
└─→ Search Engine

┌─ Redis ────────────┐
│                    │
│  ├─ Caching        │
│  ├─ Sessions       │
│  └─ Task queue     │
│                    │
└─→ Cache & Queue

┌─ PostgreSQL ───────┐
│                    │
│  ├─ Main DB        │
│  ├─ Production     │
│  └─ Connections    │
│                    │
└─→ Data Storage

┌─ SQLite ───────────┐
│                    │
│  ├─ Dev DB         │
│  ├─ Testing        │
│  └─ Single file    │
│                    │
└─→ Data Storage

All flow through:
  Django REST Framework
    ↓
  (Middleware/Authentication/Validation)
    ↓
  Apps (resumes, ai_parser, search, core)
    ↓
  External Services & Databases
```

---

## 📈 System Capacity & Performance

### **Current Configuration**

```
Development:
  • SQLite database (single file)
  • Single Django process
  • Single-threaded Celery
  • In-memory caching
  • Max users: ~10 concurrent

Production (Recommended):
  • PostgreSQL (13+)
  • Multiple Gunicorn workers
  • Redis cache layer
  • Celery worker pool
  • Load balancer
  • Max users: ~100 concurrent

Enterprise Scale:
  • PostgreSQL cluster
  • Kubernetes orchestration
  • Multiple Celery workers
  • Redis cluster
  • Elasticsearch cluster
  • CDN for static assets
  • Max users: 1000+ concurrent
```

---

## 🔐 Security Layers

```
Layer 1: Request Level
  ├─ CORS validation
  ├─ CSRF token check
  └─ Rate limiting

Layer 2: Authentication
  ├─ Django session
  ├─ JWT tokens (optional)
  └─ User permissions

Layer 3: Data Level
  ├─ Input validation
  ├─ SQL injection prevention
  ├─ File upload scanning
  └─ Output sanitization

Layer 4: Transport
  ├─ HTTPS/TLS
  ├─ Secure cookies
  └─ Header security

Layer 5: Database
  ├─ Parameterized queries
  ├─ User privileges
  ├─ Connection encryption
  └─ Regular backups
```

---

## 📊 Complete System Summary

### **By the Numbers**

```
Backend Code:
  ├─ Python files: 30+
  ├─ Lines of code: 15,000+
  ├─ Models: 4+
  ├─ Endpoints: 20+
  └─ Services: 5+

Frontend Code:
  ├─ TypeScript/React files: 50+
  ├─ Lines of code: 8,000+
  ├─ Components: 30+
  ├─ Pages: 5+
  └─ Custom hooks: 10+

Database:
  ├─ Tables: 10+
  ├─ Indices: 50+
  ├─ Fields: 100+
  └─ Relationships: Complex

Search Indices:
  ├─ Elasticsearch indices: 3+
  ├─ Analyzers: 5+
  ├─ Field mappings: 20+
  └─ Facets: 10+

External Integrations:
  ├─ OpenAI GPT
  ├─ Google Gemini
  ├─ Unstructured API
  ├─ Elasticsearch
  ├─ PostgreSQL
  ├─ Redis
  └─ Celery
```

---

**End of Complete Folder & Workflow Analysis**
