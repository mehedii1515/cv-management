"""File-specific API endpoints for pure file indexing and searching"""
import os
import logging
import mimetypes
import tempfile
import subprocess
from datetime import datetime
from typing import List, Dict, Any
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from .file_search_service import FileSearchService

logger = logging.getLogger(__name__)
file_service = FileSearchService()

@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
def view_file(request):
    """View or download a file"""
    try:
        file_path = request.GET.get('path')
        logger.info(f"Attempting to view file: {file_path} (method: {request.method})")
        
        if not file_path:
            logger.error("No file path provided")
            return Response({
                'error': 'No file path provided'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Normalize path for Windows
        file_path = os.path.normpath(file_path)
        logger.info(f"Normalized file path: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Try to find the file in the parent directory structure
            parent_path = file_path.replace('openai+gemini+unstructured+querymind+watchdog+dt search - Copy', 'openai+gemini+unstructured+querymind')
            logger.info(f"Trying alternative path: {parent_path}")
            
            if os.path.exists(parent_path):
                file_path = parent_path
                logger.info(f"Found file at alternative path: {file_path}")
            else:
                logger.error(f"File not found at either path: {file_path} or {parent_path}")
                return Response({
                    'error': f'File not found: {file_path}',
                    'tried_paths': [file_path, parent_path]
                }, status=status.HTTP_404_NOT_FOUND)
        
        # For HEAD requests, just return success if file exists
        if request.method == 'HEAD':
            response = HttpResponse()
            response['Content-Type'] = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            response['Content-Length'] = os.path.getsize(file_path)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        # Security check: Validate the file path is within allowed directories
        # Get the absolute path and normalize it
        abs_path = os.path.abspath(file_path)
        logger.info(f"Absolute path: {abs_path}")
        
        # Define allowed directories (adjust these based on your application's needs)
        allowed_dirs = [
            os.path.abspath(settings.MEDIA_ROOT),  # Media directory
            os.path.abspath(os.path.join(settings.BASE_DIR, 'media')),  # Another common location
            # Add the current project path to handle absolute paths from the frontend
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind+watchdog+dt search - Copy\\backend\\media',
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind\\backend\\media',
            # Add specific uploads directories
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind+watchdog+dt search - Copy\\backend\\media\\uploads',
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind\\backend\\media\\uploads',
            # Add parent directories
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind',
            'D:\\Office work\\Resume Parser\\openai+gemini+unstructured+querymind+watchdog+dt search - Copy',
            # Add normalized versions for Windows path flexibility
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind+watchdog+dt search - Copy/backend/media'),
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind/backend/media'),
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind+watchdog+dt search - Copy/backend/media/uploads'),
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind/backend/media/uploads'),
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind'),
            os.path.normpath('D:/Office work/Resume Parser/openai+gemini+unstructured+querymind+watchdog+dt search - Copy'),
        ]
        
        # Log all allowed directories for debugging
        logger.info(f"Allowed directories: {allowed_dirs}")
        
        # Check if the file path is within any of the allowed directories
        is_allowed = False
        
        # Special case for files in the logs
        if 'uploads' in abs_path.lower():
            logger.info(f"File is in uploads directory: {abs_path}")
            is_allowed = True
        else:
            # Standard directory check
            for allowed_dir in allowed_dirs:
                # Normalize both paths for consistent comparison
                norm_abs_path = os.path.normpath(abs_path).lower()
                norm_allowed_dir = os.path.normpath(allowed_dir).lower()
                
                logger.info(f"Checking if {norm_abs_path} starts with {norm_allowed_dir}")
                
                if norm_abs_path.startswith(norm_allowed_dir):
                    is_allowed = True
                    logger.info(f"File path is allowed under: {allowed_dir}")
                    break
        
        if not is_allowed:
            logger.warning(f"Attempted access to unauthorized file: {abs_path}")
            logger.warning(f"File path not found in any allowed directories: {allowed_dirs}")
            return Response({
                'error': 'Access denied: File is outside of allowed directories',
                'file_path': abs_path
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Determine the content type based on file extension
        content_type, encoding = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'  # Default content type
        
        logger.info(f"Serving file with content type: {content_type}")
        
        # For PDF files, ensure proper content type and headers
        if file_path.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        elif file_path.lower().endswith('.docx'):
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_path.lower().endswith('.doc'):
            content_type = 'application/msword'
        
        # Create response with proper headers for browser display
        response = FileResponse(
            open(file_path, 'rb'),
            content_type=content_type,
            as_attachment=False,
            filename=os.path.basename(file_path)
        )
        
        # Add headers to allow iframe embedding and proper display
        response['X-Frame-Options'] = 'SAMEORIGIN'  # Allow iframe from same origin
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        
        # Add CORS headers if needed for cross-origin requests
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
    except Exception as e:
        logger.error(f"Error viewing file: {e}")
        return Response({
            'error': 'Failed to view file',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_file_info(request):
    """Get file information and metadata"""
    try:
        file_path = request.GET.get('path')
        if not file_path:
            return Response({
                'error': 'No file path provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Normalize path
        file_path = os.path.normpath(file_path)
        
        if not os.path.exists(file_path):
            return Response({
                'error': f'File not found: {file_path}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get file stats
        file_stats = os.stat(file_path)
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            if file_extension == '.pdf':
                content_type = 'application/pdf'
            elif file_extension == '.docx':
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_extension == '.doc':
                content_type = 'application/msword'
            else:
                content_type = 'application/octet-stream'
        
        return Response({
            'file_name': file_name,
            'file_path': file_path,
            'file_size': file_stats.st_size,
            'file_size_formatted': f"{file_stats.st_size / (1024*1024):.2f} MB" if file_stats.st_size > 1024*1024 else f"{file_stats.st_size / 1024:.2f} KB",
            'content_type': content_type,
            'file_extension': file_extension,
            'modified_date': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            'created_date': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'can_preview': content_type in ['application/pdf', 'text/plain', 'image/jpeg', 'image/png', 'image/gif'],
            'preview_method': 'iframe' if content_type == 'application/pdf' else 'direct' if content_type.startswith('text/') or content_type.startswith('image/') else 'external'
        })
        
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return Response({
            'error': 'Failed to get file information',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST', 'GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def search_files_only(request):
    """Search files directly (not database records)"""
    try:
        # Add debugging information
        logger.info(f"Search request received - Method: {request.method}")
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request user: {request.user}")
        logger.info(f"Request authenticated: {request.user.is_authenticated if hasattr(request, 'user') else 'No user'}")
        
        # Handle GET request for testing
        if request.method == 'GET':
            return Response({
                'status': 'success',
                'message': 'Search endpoint is accessible',
                'method': request.method
            }, status=status.HTTP_200_OK)
        
        data = request.data
        query = data.get('query', '').strip()
        
        if not query:
            return Response({
                'error': 'Query parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract search parameters
        search_type = data.get('search_type', 'basic')  # basic or boolean
        page = int(data.get('page', 1))
        page_size = min(int(data.get('page_size', 20)), 100)  # Max 100 results per page
        
        # Extract filters
        filters = {}
        if data.get('file_extension'):
            filters['file_extension'] = data['file_extension']
        if data.get('file_category'):
            filters['file_category'] = data['file_category']
        if data.get('min_size'):
            filters['min_size'] = int(data['min_size'])
        if data.get('max_size'):
            filters['max_size'] = int(data['max_size'])
        if data.get('directory'):
            filters['directory'] = data['directory']
        if data.get('date_from'):
            filters['date_from'] = data['date_from']
        if data.get('date_to'):
            filters['date_to'] = data['date_to']
        if data.get('language'):
            filters['language'] = data['language']
        
        # Perform search
        if search_type == 'boolean':
            result = file_service.boolean_search_files(
                query=query,
                filters=filters,
                page=page,
                page_size=page_size
            )
        else:
            result = file_service.search_files(
                query=query,
                filters=filters,
                page=page,
                page_size=page_size
            )
        
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"File search error: {e}")
        return Response({
            'error': 'Search failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def file_suggestions(request):
    """Get file search suggestions"""
    try:
        partial_query = request.GET.get('q', '').strip()
        limit = min(int(request.GET.get('limit', 10)), 20)
        
        if len(partial_query) < 2:
            return Response({
                'suggestions': []
            }, status=status.HTTP_200_OK)
        
        suggestions = file_service.get_file_suggestions(partial_query, limit)
        
        return Response({
            'suggestions': suggestions,
            'query': partial_query
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"File suggestions error: {e}")
        return Response({
            'suggestions': [],
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def index_directory(request):
    """Index all files in a directory"""
    try:
        data = request.data
        directory_path = data.get('directory_path', '').strip()
        
        if not directory_path:
            return Response({
                'error': 'directory_path is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.exists(directory_path):
            return Response({
                'error': 'Directory does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract options
        recursive = data.get('recursive', True)
        file_extensions = data.get('file_extensions', ['.pdf', '.docx', '.doc', '.txt', '.rtf'])
        
        # Start indexing
        logger.info(f"Starting directory indexing: {directory_path}")
        result = file_service.index_directory(
            directory_path=directory_path,
            recursive=recursive,
            file_extensions=file_extensions
        )
        
        return Response({
            'message': 'Directory indexing completed',
            'results': result,
            'directory': directory_path
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Directory indexing error: {e}")
        return Response({
            'error': 'Directory indexing failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def index_single_file(request):
    """Index a single file"""
    try:
        data = request.data
        file_path = data.get('file_path', '').strip()
        
        if not file_path:
            return Response({
                'error': 'file_path is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.exists(file_path):
            return Response({
                'error': 'File does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        base_directory = data.get('base_directory')
        
        # Index the file
        success = file_service.index_file(file_path, base_directory)
        
        if success:
            return Response({
                'message': 'File indexed successfully',
                'file_path': file_path
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to index file',
                'file_path': file_path
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Single file indexing error: {e}")
        return Response({
            'error': 'File indexing failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_file_from_index(request):
    """Delete a file from the index"""
    try:
        data = request.data
        file_path = data.get('file_path', '').strip()
        
        if not file_path:
            return Response({
                'error': 'file_path is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete from index
        success = file_service.delete_file_from_index(file_path)
        
        if success:
            return Response({
                'message': 'File removed from index',
                'file_path': file_path
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to remove file from index',
                'file_path': file_path
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"File deletion error: {e}")
        return Response({
            'error': 'File deletion failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def file_search_status(request):
    """Get file search system status"""
    try:
        status_info = file_service.get_system_status()
        
        return Response({
            'status': 'active' if status_info.get('file_search_ready') else 'inactive',
            'system_info': status_info,
            'endpoints': {
                'search': '/api/files/search/',
                'suggestions': '/api/files/suggestions/',
                'index_directory': '/api/files/index/directory/',
                'index_file': '/api/files/index/file/',
                'delete_file': '/api/files/index/delete/',
                'status': '/api/files/status/'
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_file_index(request):
    """Create/recreate the file search index"""
    try:
        success = file_service.create_file_index()
        
        if success:
            return Response({
                'message': 'File index created successfully',
                'index_name': file_service.index_name
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to create file index'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Index creation error: {e}")
        return Response({
            'error': 'Index creation failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_indexed_directories(request):
    """Get list of directories that have been indexed"""
    try:
        # This would need to track indexed directories
        # For now, return basic info
        status_info = file_service.get_system_status()
        
        return Response({
            'total_files': status_info.get('total_files', 0),
            'index_ready': status_info.get('file_search_ready', False),
            'message': 'Use /api/files/search/ to search indexed files'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Directory list error: {e}")
        return Response({
            'error': 'Failed to get directory information',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Upload and index file endpoint
@api_view(['POST'])
def upload_and_index_file(request):
    """Upload a file and immediately index it"""
    try:
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({
                'error': 'No file uploaded'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save uploaded file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'file_index_uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Index the uploaded file
        success = file_service.index_file(file_path, upload_dir)
        
        if success:
            return Response({
                'message': 'File uploaded and indexed successfully',
                'filename': uploaded_file.name,
                'file_path': file_path,
                'file_size': uploaded_file.size
            }, status=status.HTTP_201_CREATED)
        else:
            # Remove file if indexing failed
            try:
                os.remove(file_path)
            except:
                pass
                
            return Response({
                'error': 'File uploaded but indexing failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Upload and index error: {e}")
        return Response({
            'error': 'File upload and indexing failed',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_file_content(request):
    """Get extracted text content from indexed files"""
    try:
        file_path = request.GET.get('path')
        logger.info(f"Attempting to get content for file: {file_path}")
        
        if not file_path:
            logger.error("No file path provided")
            return Response({
                'error': 'No file path provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Normalize path for Windows
        file_path = os.path.normpath(file_path)
        logger.info(f"Normalized file path: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return Response({
                'error': f'File not found: {file_path}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Try to get content from search index first
        try:
            search_results = file_service.search_files(
                query="*",
                filters={'file_path': file_path},
                page_size=1
            )
            
            if search_results and search_results.get('files') and len(search_results['files']) > 0:
                indexed_file = search_results['files'][0]
                extracted_text = indexed_file.get('content', '')
                
                if extracted_text:
                    logger.info(f"Found extracted content in search index")
                    return Response({
                        'success': True,
                        'extracted_text': extracted_text,
                        'file_path': file_path,
                        'source': 'search_index'
                    })
        
        except Exception as search_error:
            logger.warning(f"Could not get content from search index: {search_error}")
        
        # Fallback: Extract content directly from file
        try:
            from .file_documents import FileDocument
            
            file_extension = os.path.splitext(file_path)[1].lower()
            extracted_text = ""
            
            if file_extension == '.pdf':
                extracted_text = FileDocument.extract_pdf_text(file_path)
            elif file_extension in ['.docx', '.doc']:
                extracted_text = FileDocument.extract_word_text(file_path)
            elif file_extension in ['.txt', '.rtf']:
                extracted_text = FileDocument.extract_plain_text(file_path)
            
            if extracted_text:
                logger.info(f"Extracted content directly from file")
                return Response({
                    'success': True,
                    'extracted_text': extracted_text,
                    'file_path': file_path,
                    'source': 'direct_extraction'
                })
            else:
                logger.warning(f"No content could be extracted from file")
                return Response({
                    'error': 'Could not extract text content from file',
                    'file_path': file_path
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        except Exception as extraction_error:
            logger.error(f"Error extracting content: {extraction_error}")
            return Response({
                'error': 'Failed to extract content from file',
                'message': str(extraction_error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        logger.error(f"Error getting file content: {e}")
        return Response({
            'error': 'Failed to get file content',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# DOCX to PDF conversion system removed per user request

# DOCX to PDF conversion system removed per user request
