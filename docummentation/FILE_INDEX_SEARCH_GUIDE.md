# DTSearch File Index Search Features

## Overview
The file index search functionality provides DTSearch-like capabilities for searching through the actual content of uploaded resume files (PDF, DOCX, DOC, TXT). This is in addition to the existing database field search.

## File Search Capabilities

### 1. File Content Indexing
- **Full-text indexing** of uploaded resume files
- **Multi-format support**: PDF, DOCX, DOC, TXT
- **Automatic text extraction** using multiple parsers:
  - PDF: `pypdf` library for PDF text extraction
  - DOCX: `unstructured` library for modern Word documents
  - DOC: `unstructured` library for legacy Word documents
  - TXT: Native text file reading with encoding detection

### 2. File Metadata Storage
Each indexed file includes:
- `filename`: Original filename
- `file_path`: Full system path to file
- `file_size`: File size in bytes
- `file_type`: File extension (.pdf, .docx, .doc, .txt)
- `content_hash`: MD5 hash for duplicate detection
- `indexed_date`: When the file was indexed
- `extracted_text`: Full text content of the file

### 3. Advanced File Search API

#### Basic File Search
```bash
GET /api/search/files/?q=python+developer
```

#### File Search with Filters
```bash
# By file type
GET /api/search/files/?q=java&file_type=.pdf

# By file size (in bytes)
GET /api/search/files/?q=react&min_size=50000&max_size=500000

# By filename
GET /api/search/files/?q=django&filename=senior

# By date range
GET /api/search/files/?q=manager&date_from=2024-01-01&date_to=2024-12-31

# Combined filters
GET /api/search/files/?q=python&file_type=.docx&min_size=100000
```

#### POST Request for Complex Filters
```bash
curl -X POST http://localhost:8000/api/search/files/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning", 
    "filters": {
      "file_type": ".pdf",
      "min_file_size": 100000,
      "max_file_size": 1000000
    }
  }'
```

### 4. Frontend Integration

#### File Search Panel Component
The `FileSearchPanel` component provides:
- **File-specific search interface** with content search
- **Advanced filtering options**:
  - File type dropdown (PDF, DOCX, DOC, TXT)
  - Filename contains filter
  - File size range (min/max in KB)
  - Date range filters (indexed after/before)
- **Rich result display** with file metadata
- **Content preview** showing extracted text snippets
- **File type icons** for visual identification
- **File size formatting** (B, KB, MB, GB)

#### Usage in Dashboard
```typescript
import { FileSearchPanel } from '@/components/FileSearchPanel'

<FileSearchPanel 
  onSelectResult={(result) => {
    console.log('Selected file:', result)
    // Handle file selection
  }}
/>
```

## API Response Format

### File Search Response Structure
```json
{
  "hits": [
    {
      "id": "resume-id",
      "score": 8.59,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "location": "New York",
      "skills": "Python, Django, React",
      
      // File-specific metadata
      "filename": "john_doe_resume.pdf",
      "file_type": ".pdf", 
      "file_size": 245760,
      "file_size_mb": 0.23,
      "indexed_date": "2024-08-07T10:30:00Z",
      "content_preview": "Software Engineer with 5+ years...",
      
      // Search highlights
      "highlights": {
        "extracted_text": ["<mark>Python</mark> developer with expertise"],
        "filename": ["<mark>john</mark>_doe_resume.pdf"],
        "skills": ["<mark>Python</mark>, Django, React"]
      }
    }
  ],
  "total_hits": 15,
  "max_score": 8.59,
  "took": 45,
  "search_info": {
    "query": "python",
    "filters_applied": {"file_type": ".pdf"},
    "search_type": "file_search",
    "file_types_found": [".pdf", ".docx"],
    "size_range": {
      "min_size_mb": 0.1,
      "max_size_mb": 2.5
    },
    "search_time_ms": 45
  }
}
```

## Search Features

### 1. Content-First Search
File search prioritizes actual file content over database fields:
```
Field Boosting:
- extracted_text^2.0    (highest priority - actual file content)
- name^1.8               (person name)
- skills^1.5             (skills from database)
- experience^1.3         (experience from database)
- filename^1.0           (filename matching)
- email^0.8              (email matching)
```

### 2. Highlighting
Search results include highlighting for:
- **File content**: Matched text from the actual document
- **Filename**: Matched parts of the filename
- **Database fields**: Name, skills, experience matches
- **Fragment size**: 200 characters per highlight
- **Multiple fragments**: Up to 3 fragments per field

### 3. File Filtering
Advanced filtering options:
- **File type**: Exact file extension matching
- **File size**: Range filtering (min/max in bytes)
- **Filename**: Partial filename matching
- **Date range**: Indexed date filtering
- **Content-based**: Search within extracted text

## Use Cases

### 1. Document Content Search
Find resumes containing specific technologies mentioned in the actual document:
```bash
GET /api/search/files/?q=kubernetes+docker&file_type=.pdf
```

### 2. File Management
Find large files or specific file types:
```bash
GET /api/search/files/?q=*&min_size=1000000&file_type=.docx
```

### 3. Duplicate Detection
Using content hash for finding duplicate files:
```bash
# Content hash is automatically generated and can be used for deduplication
```

### 4. Recent File Search
Find recently indexed files:
```bash
GET /api/search/files/?q=python&date_from=2024-08-01
```

## Technical Implementation

### Backend Components

#### Document Indexing (`apps/search/documents.py`)
- `CVDocument` class with file metadata fields
- Automatic text extraction methods for each file type
- Content hash generation for duplicate detection
- File metadata preparation methods

#### Search Service (`apps/search/services.py`)
- Enhanced query building with file content priority
- File-specific filtering in `_apply_filters()`
- File metadata in search result formatting
- Content preview generation

#### API Views (`apps/search/views.py`)
- `file_search()` endpoint for dedicated file search
- File filter parameter processing
- File metadata enrichment in responses

### Frontend Components

#### FileSearchPanel (`components/FileSearchPanel.tsx`)
- Dedicated file search interface
- Advanced filter controls
- File metadata display
- Content preview rendering

#### Integration (`app/page.tsx`)
- File search tab in main navigation
- Combined with existing search options
- Seamless user experience

## Configuration and Setup

### 1. Backend Requirements
```python
# requirements.txt additions for file processing
pypdf>=3.0.0
unstructured>=0.10.0
python-docx>=0.8.11
```

### 2. Elasticsearch Index Recreation
After adding file search capabilities, recreate the index:
```bash
curl -X POST http://localhost:8000/api/search/create-index/
```

### 3. File Upload Integration
Ensure resume uploads trigger file indexing:
```python
# In resume upload views/signals
from apps.search.documents import CVDocument
# Trigger document indexing after file upload
```

### 4. Frontend Proxy Configuration
```javascript
// next.config.js
{
  source: '/api/search/files',
  destination: 'http://localhost:8000/api/search/files/',
}
```

## Performance Considerations

### 1. File Processing
- **Async processing**: Large files processed in background
- **Error handling**: Graceful fallback for unsupported formats
- **Memory management**: Streaming for large files
- **Cache utilization**: 5-minute cache for repeat searches

### 2. Index Optimization
- **Field mapping**: Optimized for search and storage
- **Shard configuration**: Single shard for small to medium datasets
- **Replica settings**: No replicas for development

### 3. Search Performance
- **Query optimization**: Multi-match with field boosting
- **Pagination**: Configurable page sizes (10, 20, 50)
- **Result limiting**: Reasonable fragment sizes for highlighting

## Future Enhancements

### 1. Advanced File Features
- **OCR support**: Scan images in PDFs for text
- **Metadata extraction**: Creation date, author, etc.
- **File versioning**: Track file updates and changes
- **Thumbnail generation**: Preview images for documents

### 2. Search Improvements
- **Fuzzy matching**: Better handling of typos in file content
- **Semantic search**: AI-powered content understanding
- **Similar document finding**: Content-based recommendations
- **Auto-categorization**: ML-based file classification

### 3. User Experience
- **File preview**: In-browser document viewing
- **Download links**: Direct file access from search results
- **Bulk operations**: Multi-file actions
- **Search analytics**: Usage tracking and optimization

## Troubleshooting

### Common Issues

1. **Empty File Metadata**
   - Ensure files are actually uploaded and stored
   - Check file path accessibility
   - Verify text extraction libraries are installed

2. **No Search Results**
   - Verify Elasticsearch is running
   - Check index exists and contains documents
   - Confirm file content extraction is working

3. **Slow Search Performance**
   - Review query complexity and filters
   - Check index size and shard configuration
   - Monitor Elasticsearch cluster health

### Debug Commands
```bash
# Check system status
curl http://localhost:8000/api/search/status/

# Test basic search
curl "http://localhost:8000/api/search/files/?q=test"

# Recreate index if needed
curl -X POST http://localhost:8000/api/search/create-index/

# Check Elasticsearch directly
curl http://localhost:9200/_cat/indices
```

This comprehensive file search system provides DTSearch-like functionality for resume files, enabling powerful content-based search capabilities alongside the existing database field search.
