# File Viewer Implementation Guide

## Overview
The file viewer has been enhanced to display PDF, DOCX, DOC, and other file types directly in the browser instead of showing just extracted text.

## Key Changes Made

### 1. Frontend FileViewer Component (`frontend/src/components/FileViewer.tsx`)

#### Enhanced File Type Handling:
- **PDF Files**: Direct embedding using `<iframe>` with proper PDF content-type
- **Word Documents**: Multiple fallback viewers:
  1. Microsoft Office Online Viewer (primary)
  2. Google Docs Viewer (fallback)
  3. Download option (final fallback)
- **Images**: Direct display with proper sizing
- **Text Files**: Formatted display with monospace font

#### Features Added:
- Better loading states with spinner
- Error handling with retry functionality
- Responsive design for different screen sizes
- Proper error messages for unsupported formats

### 2. Backend Enhancements (`backend/apps/search/file_views.py`)

#### Improved Content Type Handling:
```python
# Explicit content-type mapping for better browser recognition
if file_extension == '.pdf':
    content_type = 'application/pdf'
elif file_extension == '.docx':
    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
elif file_extension == '.doc':
    content_type = 'application/msword'
```

#### Enhanced Response Headers:
- CORS headers for cross-origin requests
- `Content-Disposition: inline` for browser viewing
- `X-Frame-Options: SAMEORIGIN` for iframe embedding

#### New API Endpoint Added:
- `/api/search/files/info` - Returns file metadata and preview capabilities

### 3. File Type Support Matrix

| File Type | Extension | Display Method | Status |
|-----------|-----------|----------------|---------|
| PDF | `.pdf` | Direct iframe embedding | ✅ Fully Supported |
| Word (Modern) | `.docx` | Office Online Viewer → Google Docs → Download | ✅ Multiple Fallbacks |
| Word (Legacy) | `.doc` | Office Online Viewer → Google Docs → Download | ✅ Multiple Fallbacks |
| Text | `.txt` | Direct text display | ✅ Fully Supported |
| Images | `.jpg`, `.png`, `.gif` | Direct image display | ✅ Fully Supported |
| Others | Various | Google Docs Viewer → Download | ⚠️ Limited Support |

## Usage Instructions

### For Users:
1. **Search for files** using the File Index Search tab
2. **Click on any search result** to open the file viewer
3. **PDF files** will load directly in the browser
4. **Word documents** will attempt multiple viewing methods
5. **Download button** is always available as backup

### For Developers:

#### Testing File Viewer:
```javascript
// Test the file info endpoint
fetch('/api/search/files/info?path=/path/to/your/file.pdf')
  .then(response => response.json())
  .then(data => console.log('File info:', data))

// Test direct file viewing
window.open('/api/search/files/view?path=/path/to/your/file.pdf', '_blank')
```

#### Debugging Steps:
1. **Check browser console** for any iframe loading errors
2. **Verify CORS headers** in Network tab
3. **Test file accessibility** by trying direct URL
4. **Check server logs** for file path resolution issues

## Known Limitations

### Word Document Viewing:
- **Office Online Viewer** requires internet connection
- **Google Docs Viewer** has file size limitations
- **Some corporate firewalls** may block external viewers
- **Very large files** may timeout during loading

### PDF Viewing:
- **Browser PDF support** varies by browser
- **Some mobile browsers** may force download instead of display
- **Password-protected PDFs** will not display

## Troubleshooting

### Common Issues:

#### "File not found" Error:
- Check file path is correct in search results
- Verify file still exists on disk
- Check backend file path resolution logs

#### PDF Not Displaying:
- Verify browser supports PDF viewing
- Check if PDF is corrupted
- Try downloading the file directly

#### Word Document Shows Blank/Error:
- Check internet connectivity (for online viewers)
- Try the download option
- Verify file is a valid Word document

#### CORS Errors:
- Ensure backend CORS headers are properly set
- Check if frontend and backend are on same domain
- Verify API endpoint configuration

### Debug Mode:
Enable debug logging by checking browser console. The file viewer logs:
- File loading attempts
- Viewer fallback attempts
- Error messages and status codes

## Future Enhancements

### Planned Features:
1. **Offline PDF.js viewer** for better PDF support
2. **Document thumbnails** in search results  
3. **Full-screen viewing mode**
4. **Annotation support** for PDFs
5. **Print functionality** from viewer
6. **Mobile-optimized viewing**

### Performance Improvements:
1. **Lazy loading** for large files
2. **Caching** for frequently accessed files
3. **Progressive loading** for multi-page documents
4. **Bandwidth optimization** for mobile users

## Technical Implementation Details

### Frontend Architecture:
```typescript
interface FileViewerProps {
  filePath: string | null    // Full path to file
  fileName?: string          // Display name
  onClose: () => void       // Close handler
}
```

### Backend API Endpoints:
- `GET /api/search/files/view?path=<file_path>` - Serve file content
- `GET /api/search/files/info?path=<file_path>` - Get file metadata

### Security Considerations:
- **Path traversal protection** in backend
- **Allowed directory validation**
- **Content-type verification**
- **File size limitations**

This implementation provides a robust file viewing experience while maintaining security and handling various edge cases gracefully.
